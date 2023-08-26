# BSc Final Project - IoT Wildlife and Intrusion Detection System - Django Component

Welcome to the Django component repository of the IoT Wildlife and Intrusion Detection System!

The Arduino repository can be found at <a href="https://github.com/wbrocker/FP-Arduino-Code">FP-Arduino-Code</a>.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Contributions](#contributions)
- [License](#license)

## Introduction

This repository contains the Django component of the IoT Wildlife and Intrusion Detection System. This system aims to enhance security and safety in rural areas by detecting intrusions from both wildlife and unauthorized individuals. The Django component serves as the main controller and user interface for the entire system.

## Features

- Comprehensive user dashboard for system configuration and monitoring
- Device registration and management
- Alarm setup and monitoring
- Audit log for tracking system activities
- Integration with ESP32-Cam and ESP8266 Arduino components
- RESTful API for device registration and configuration
- MQTT for real-time updates and communication with Arduino components

## Getting Started

### Prerequisites

- Python 3.x
- Django
- SQLite (used as the database)
- paho-mqtt library for MQTT communication
- Other dependencies listed in requirements.txt

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/FP-Django.git

2. Navigate to the Project directory:
    
    ```bash
    cd FP-Django

3. Install the dependencies:
    
    ```bash
    pip install -r requirements.txt


### Configuration

1. Configure the database settings in `settings.py`.
2. Adjust any necessary settings for MQTT communication in `settings.py`.

## Usage

1. Run the Django development server:

    ```bash
    python manage.py runserver 0.0.0.0:8000

2. Access the dashboard by opening your web browser and navigating to:
    `http://localhost:8000`.

3. Explore the various features of the dashboard, including device management, alarm setup, and audit logs.

## Contributions

This project was developed for academic purposes as part of a BSc course. Currently, I am 
not accepting external contributions or pull requests. However, if you have suggestions,
questions, or feedback, please feel free to open an issue. Your insights could be valuable
for potential future enhancements.

## License

This project is licensed under the [MIT License](LICENSE).