## **Project Overview**
This project is designed for personal usage and is intended to be used with the Nextcloud calendar, although it should theoretically be compatible with other webcal services as well.

## **Twitch Credentials**
1. To set up Twitch credentials for this project, follow these steps:

2. Go to the Twitch Developer Console and enable two-factor authentication (2FA).

3. Create a new application with a unique name to avoid potential SQL errors without clear visual feedback.

4. Obtain your client ID and client secret after setting up the application.

5. Use the following curl command to obtain your bearer token:

    ```bash
    curl -X POST 'https://id.twitch.tv/oauth2/token' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'client_id=<your client id goes here>&client_secret=<your client secret goes here>&grant_type=client_credentials'
    ```

6. Save the resulting access token and client ID for use in the docker-compose.yaml file.

## **Good to Know**

Currently, CalDAV does not offer support for searching events by ID. Therefore, prior to any updates, the script deletes all events on the calendar. To address this, I recommend using a separate Twitch calendar to ensure that no important events disappear during the refresh.

## **Environment Setup**

To configure the environment for this project:

Edit the docker-compose.yaml file with your Nextcloud and Twitch details.
Specify the Nextcloud details and Twitch preferences within this file to ensure the script functions correctly.
Feel free to reach out if you encounter any issues or need further assistance with setup!

