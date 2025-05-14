#!/usr/bin/env bash

# Update package lists
apt-get update

# Install prerequisites
apt-get install -y curl apt-transport-https gnupg

# Add Microsoft repository for ODBC Driver 18
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Update package lists again
apt-get update

# Install ODBC Driver 18 for SQL Server
ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Install unixODBC development headers
apt-get install -y unixodbc-dev