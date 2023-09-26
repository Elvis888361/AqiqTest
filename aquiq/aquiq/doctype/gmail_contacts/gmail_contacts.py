# Copyright (c) 2023, Aquiq and contributors
# For license information, please see license.txt

import frappe
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from frappe.model.document import Document
from frappe import _

class GmailContacts(Document):
    pass

@frappe.whitelist()
def get_contact():
    # Scopes for accessing Gmail and Google Contacts
    SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

    def authenticate_google_contacts():
        # Create or load token.pickle to store user's credentials
        token_file = 'token.pickle'
        creds = None
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, ask the user to log in
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sites/secrets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        # Build the Google Contacts service
        service = build('people', 'v1', credentials=creds)
        return service

    def retrieve_contact_numbers():
        service = authenticate_google_contacts()
        numbers = []

        # Fetch the user's contact list
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,  # Adjust as needed
            personFields='names,phoneNumbers').execute()
        connections = results.get('connections', [])

        if not connections:
            frappe.msgprint('No connections found.')
            return []

        frappe.msgprint('Contact Numbers:')
        for person in connections:
            if 'phoneNumbers' in person:
                contact_numbers = []
                for phoneNumber in person['phoneNumbers']:
                    name = person.get('names', [{}])[0].get('displayName', 'Unknown')
                    number = phoneNumber.get('value')
                    contact_numbers.append(number)
                    frappe.msgprint(f"{name}: {number}")
                numbers.extend(contact_numbers)
            else:
                frappe.msgprint("No phone numbers found for this contact.")

        if not numbers:
            frappe.msgprint("No phone numbers found for any contact.")
        return numbers

    return retrieve_contact_numbers()
