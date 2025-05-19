# gcPanel Integrations Module Documentation

This document provides detailed information about the gcPanel Integrations Module, including how to set up external service connections, import data, and synchronize with external platforms.

## Table of Contents

1. [Overview](#overview)
2. [Supported Platforms](#supported-platforms)
3. [Setting Up Integrations](#setting-up-integrations)
4. [Importing Data](#importing-data)
5. [Data Synchronization](#data-synchronization)
6. [Technical Implementation](#technical-implementation)
7. [Troubleshooting](#troubleshooting)

## Overview

The gcPanel Integrations Module provides a comprehensive system for connecting with external construction management platforms, importing data, and keeping project information synchronized. This allows teams to leverage data from specialized tools while maintaining a single source of truth within gcPanel.

## Supported Platforms

The following external platforms are currently supported:

| Platform | Data Types | Authentication Method |
|----------|------------|----------------------|
| Procore | Documents, Specifications, Bids, Daily Reports, Budget, Schedule, Incidents | OAuth 2.0 |
| PlanGrid | Documents, Daily Reports | API Key |
| FieldWire | Documents, Daily Reports | API Key |
| BuildingConnected | Bids | OAuth 2.0 |

## Setting Up Integrations

### Steps to Connect a Platform

1. Navigate to **Settings > Integrations**
2. Find the platform you want to connect
3. Click "Connect" 
4. Enter the required credentials:
   - For OAuth platforms: Client ID and Client Secret
   - For API Key platforms: API Key and any additional required fields
5. Click "Connect" to establish the connection

### Obtaining API Credentials

#### Procore
1. Log in to your Procore account
2. Navigate to your company's Admin section
3. Go to the Developer Portal
4. Create a new application to get Client ID and Client Secret

#### PlanGrid
1. Log in to your PlanGrid account
2. Go to Account Settings
3. Navigate to the API section
4. Generate a new API Key

#### FieldWire
1. Log in to your FieldWire account
2. Go to Account Settings
3. Navigate to the Integrations section
4. Generate a new API Key

#### BuildingConnected
1. Log in to your BuildingConnected account
2. Go to your account settings
3. Navigate to the Developer section
4. Create a new application to get Client ID and Client Secret

## Importing Data

### Import Process

1. Navigate to **Integrations** in the main menu
2. Select the "Import Data" tab
3. Choose the platform to import from (must be connected)
4. Select the data type to import
5. Choose the import method:
   - **Merge**: Add new data while updating existing records
   - **Replace**: Remove all existing data of this type and replace with new data
6. Click "Start Import" to begin the process
7. Review the preview of data before confirming

### Data Types

Each platform supports different types of data that can be imported:

- **Documents**: Project files, drawings, and attachments
- **Specifications**: Technical specifications for project elements
- **Bids**: Bid submissions and bidding information
- **Daily Reports**: Site activity logs and progress reports
- **Budget**: Financial information and cost tracking
- **Schedule**: Project timeline and task scheduling
- **Incidents**: Safety incidents and related documentation

## Data Synchronization

### Manual Sync

1. Navigate to **Integrations** in the main menu
2. Select the "Sync Status" tab
3. Choose the platform and data type to synchronize
4. Click "Sync Now" to manually update the data

### Sync Status

The Sync Status tab provides information about:
- Last connection time for each platform
- Last import date for each data type
- Number of records imported by type
- Status of each integration

## Technical Implementation

The integration system is built with a modular architecture consisting of:

1. **Authentication Module**: Handles secure authentication with external services
2. **Import Manager**: Facilitates data import and preview
3. **Data Persistence**: Manages storage and retrieval of imported data
4. **Synchronization**: Coordinates data updates between platforms

The system is designed to gracefully handle connectivity issues and provide fallback mechanisms when external services are unavailable.

## Troubleshooting

### Common Issues

#### Connection Failures
- Verify that your API credentials are correct and not expired
- Check that you have the necessary permissions in the external platform
- Ensure your account is active and in good standing

#### Import Errors
- Confirm that the data you're trying to import exists in the source platform
- Check for any rate limits or API usage restrictions
- For large datasets, try importing in smaller batches

#### Synchronization Problems
- Verify that both systems are online and accessible
- Check for any field mapping issues between platforms
- Ensure that data formats are compatible

### Getting Help

If you encounter issues with integrations:
1. Check the application logs for detailed error messages
2. Contact your system administrator with specific error details
3. Refer to the external platform's API documentation for guidance
