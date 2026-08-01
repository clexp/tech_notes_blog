#!/bin/bash

# Blog deployment script with password variable
# Set your password once and avoid multiple prompts

set -e  # Exit on any error

# Configuration
FREEBSD_HOST="10.0.0.50"
FREEBSD_USER="clexp"
STAGING_DIR="/tmp/blog-files"
NGINX_DOCUMENT_ROOT="/usr/jails/nginx/usr/local/www/nginx-dist"
SITE_URL="https://blog.clexp.net"

# Set your password here (or export it as environment variable)
FREEBSD_PASSWORD=""
# Alternative: export FREEBSD_PASSWORD="your_password" before running

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if password is set
check_password() {
    if [ -z "$FREEBSD_PASSWORD" ]; then
        log_error "Password not set. Please set FREEBSD_PASSWORD variable or edit this script."
        echo "You can either:"
        echo "1. Edit this script and set FREEBSD_PASSWORD='your_password'"
        echo "2. Run: export FREEBSD_PASSWORD='your_password' && ./deploy_with_password.sh"
        exit 1
    fi
}

# SSH function with password
ssh_with_password() {
    local cmd="$1"
    sshpass -p "$FREEBSD_PASSWORD" ssh -o StrictHostKeyChecking=no "${FREEBSD_USER}@${FREEBSD_HOST}" "$cmd"
}

# SCP function with password
scp_with_password() {
    local src="$1"
    local dest="$2"
    sshpass -p "$FREEBSD_PASSWORD" scp -o StrictHostKeyChecking=no -r "$src" "$dest"
}

# Check if zola is installed
check_zola() {
    if ! command -v zola &> /dev/null; then
        log_error "Zola is not installed or not in PATH"
        exit 1
    fi
}

# Check if sshpass is installed
check_sshpass() {
    if ! command -v sshpass &> /dev/null; then
        log_error "sshpass is not installed. Install it with: brew install sshpass"
        exit 1
    fi
}

# Build the site
build_site() {
    log_info "Building Zola site..."
    
    # Clean previous build
    if [ -d "public" ]; then
        rm -rf public
        log_info "Cleaned previous build"
    fi
    
    # Build site
    zola build
    
    if [ $? -eq 0 ]; then
        log_success "Site built successfully"
        log_info "Generated $(find public -type f | wc -l) files"
    else
        log_error "Failed to build site"
        exit 1
    fi
}

# Copy files to FreeBSD staging
copy_to_staging() {
    log_info "Copying files to FreeBSD staging area..."
    
    # Create staging directory on remote host
    ssh_with_password "mkdir -p ${STAGING_DIR}"
    
    # Copy files
    scp_with_password "public/*" "${FREEBSD_USER}@${FREEBSD_HOST}:${STAGING_DIR}/"
    
    if [ $? -eq 0 ]; then
        log_success "Files copied to staging area"
    else
        log_error "Failed to copy files to staging"
        exit 1
    fi
}

# Deploy to nginx document root
deploy_to_nginx() {
    log_info "Deploying to nginx document root..."
    
    # Step 1: Copy files
    log_info "Step 1: Copying files to nginx document root..."
    ssh_with_password "doas cp -r ${STAGING_DIR}/* ${NGINX_DOCUMENT_ROOT}/"
    
    if [ $? -ne 0 ]; then
        log_error "Failed to copy files to nginx document root"
        exit 1
    fi
    
    # Step 2: Set ownership
    log_info "Step 2: Setting proper ownership..."
    ssh_with_password "doas chown -R www:www ${NGINX_DOCUMENT_ROOT}/"
    
    if [ $? -ne 0 ]; then
        log_error "Failed to set file ownership"
        exit 1
    fi
    
    # Step 3: Reload nginx
    log_info "Step 3: Reloading nginx in jail..."
    ssh_with_password "doas jexec nginx service nginx reload"
    
    if [ $? -ne 0 ]; then
        log_error "Failed to reload nginx"
        exit 1
    fi
    
    # Step 4: Clean up
    log_info "Step 4: Cleaning up staging files..."
    ssh_with_password "rm -rf ${STAGING_DIR}/*"
    
    log_success "Deployment completed successfully"
}

# Verify deployment
verify_deployment() {
    log_info "Verifying deployment..."
    
    # Check if contact page exists
    log_info "Checking for contact page..."
    ssh_with_password "ls -la ${NGINX_DOCUMENT_ROOT}/contact/ 2>/dev/null && echo 'Contact page found!' || echo 'Contact page not found'"
    
    # Test local nginx response
    log_info "Testing local nginx response..."
    ssh_with_password "curl -s -I http://10.100.0.5/ | head -1"
    
    # Test public site
    log_info "Testing public site..."
    if curl -s -I "${SITE_URL}" | head -1 | grep -q "200 OK"; then
        log_success "Public site is responding correctly"
    else
        log_warning "Public site test failed or not immediately available"
    fi
}

# Main deployment function
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}    Blog Deployment Script${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    
    # Check prerequisites
    check_password
    check_zola
    check_sshpass
    
    # Show deployment info
    echo -e "${YELLOW}Deployment target:${NC} ${SITE_URL}"
    echo -e "${YELLOW}FreeBSD host:${NC} ${FREEBSD_HOST}"
    echo -e "${YELLOW}Document root:${NC} ${NGINX_DOCUMENT_ROOT}"
    echo -e "${YELLOW}New features:${NC} Contact page, updated navigation"
    echo
    
    # Confirm deployment
    read -p "Continue with deployment? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Deployment cancelled"
        exit 0
    fi
    
    # Execute deployment steps
    echo
    log_info "Starting deployment process..."
    
    build_site
    copy_to_staging
    deploy_to_nginx
    verify_deployment
    
    echo
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}    Deployment Completed Successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo
    echo -e "${BLUE}🌐 Main Site:${NC} ${SITE_URL}"
    echo -e "${BLUE}📞 Contact Page:${NC} ${SITE_URL}/contact/"
    echo -e "${BLUE}🔍 Search:${NC} Now available on all pages"
    echo
    log_success "Your blog is now live with all the latest updates!"
}

# Error handling
trap 'log_error "Deployment failed at step: $BASH_COMMAND"' ERR

# Run main function
main "$@" 