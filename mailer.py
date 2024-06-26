import django
import os
import imaplib
import email
import re
from django.core.mail import send_mail
import smtplib
import asyncio
import json

# Specify the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iterio_project.settings')

# Initialize Django
django.setup()

class connection:
    """This class contains everything needed to validate email via welcome message\n
        Methods:
            start(): starts the connection to email with imaplib
            stop(): stops the connection and logsout with imaplib
            clean(): deletes all found fail sent emails by google
            read_json(): retrives data from json that contains invalid emails
            save_json(): save invalid emails to json file
            is_email_valid(): validates email, using the welcome message as decoy
            welcome_msg(): sends welcome msg to new iterio users
    """

    #imap will hold the connection to email via imaplib
    imap = None
    msgIds = None

    async def start(time: float = 0.0) -> None:
        """Starts a connection to email inbox using imap\n
            Execeptions - when login to email fails:
        """
        if time < 0.0:
            time = 0.0
        print("\t--->Starting connection to INBOX<---")
        connection.imap = imaplib.IMAP4_SSL("imap.gmail.com")
        bot = "iterio.supp@gmail.com"
        key = "nsnx vvfl snyr xwtb"
        try:
            connection.imap.login(bot, key)
            await asyncio.sleep(time)
            connection.imap.select("INBOX")
            print("\t---> Connected Succesfully <---\n\t--")
        except Exception as e:
            print(f"Fail to login: {e}")


    async def stop() -> None:
        """Stops the connections with email and logsout
        """
        print("\t---> Stoping Connection, loginout <---\n\t--")
        connection.imap.close()
        connection.imap.logout()
        connection.imap = None


    async def clean(time: float = 0.0) -> None:
        """Deletes all error mails in the email inbox
            Args:
                time: delay the deleting process
        """
        if time < 0.0:
            time = 0.0
        if not connection.imap:
            await connection.start()
        print("\t---> Deleting inbox mail errors <---")
        await asyncio.sleep(time)
        _, connection.msgIds = connection.imap.search(None, "ALL")
        for msgId in connection.msgIds[0].split():
            _, data = connection.imap.fetch(msgId, "(RFC822)")
            for response in data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    if msg["Subject"] == "Delivery Status Notification (Failure)":
                        connection.imap.store(msgId, '+FLAGS', '\\Deleted')
        try:
            connection.imap.expunge()
        except Exception as err:
            print(f"Fail to delete error mail: {err}")
        print("\t---> Finish deleting inbox <---\n\t--")
        await connection.stop()


    # async def mail_status() -> bool:
    #     """Verify that mail was has been sent succesfully\n
    #         Returns - True if mail was sent propertly, False otherwise
    #     """
    #     if not connection.imap:
    #         await connection.start(15)
    #     await connection.email_status()
    #     print("\t---> Verifing email <---")
    #     email_status: bool = True
    #     _, connection.msgIds = connection.imap.search(None, "ALL")
    #     _, response = connection.imap.search(None, '(SUBJECT "%s")' % "Delivery Status Notification (Failure)")
    #     invalid = response[0].decode().split()
    #     if invalid:
    #         email_status = False
    #     else:
    #         email_status = True
    #     print(f"\t\t|STATUS|\n\t--->>> Is Email Valid: {email_status} <<<---\n\t--")
    #     await connection.clean(1.0)
    #     return email_status
    
    async def read_json() -> dict:
        """tries to read json file and retrive data
            Returns:
                a dictionary with the deserialize data
        """
        content = {}
        try:
            with open("invalid_emails.json", "r") as file:
                content = json.load(file)
        except:
            print("\t\t>>> Couldn't load json <<<\n\t--")
        finally:
            return content
    
    async def save_json(content: dict = {}) -> None:
        """saves content to json file, that contains invalid emails
            Args:
                content: a dictioanry of the invalid emails found
        """
        try:
            print("\t---> Saving invalid email <---\n")
            with open("invalid_emails.json", 'w') as file:
                json.dump(content, file, indent=2)
        except:
            print("\t>>> Something went wrong saving json <<<\n\t--")

    async def is_email_valid() -> tuple:
        """Uses imaps to open email and verify for google failed msg, True if valid, False otherwise
            Returns:
                tuple with the found invalid email and the status of the search
        """
        invalid_email = "unknown-email"
        try:
            await connection.start(15)
            
            # Search for failure notifications
            _, messages = connection.imap.search(None, '(SUBJECT "Delivery Status Notification (Failure)")')
            messages = messages[0].decode('utf-8').split()

            if not messages:
                print(f"\t\t|STATUS|\n\t--->>> Is Email Valid: {True} <<<---\n\t--")
                return (True, "Valid")
            
            for msg_id in messages:
                _, msg = connection.imap.fetch(msg_id, '(RFC822)')
                raw_msg = msg[0][1].decode('utf-8')
                message = email.message_from_string(raw_msg)
                
                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                else:
                    body = message.get_payload(decode=True).decode('utf-8')

                # Extract the invalid email address from the body
                match = re.search(r"Your message wasn't delivered to ([^@]+@[^ ]+) because the address", body)
                if not match:
                    match = re.search(r"Your message wasn't delivered to ([^@]+@[^ ]+) because the domain", body)
                if match:
                    invalid_email = match.group(1)
                    print(f"\t---> Invalid email address: {invalid_email} <---\n\t--")
                else:
                    print("\t>>> Couldn't find invalid email address in the message body! <<<\n\t--")
        finally:
            await connection.clean()
            return (False, invalid_email)

    async def welcome_msg(username: str, user_email: str = None) -> tuple:
        """ Sends a welcome email to user_email
            Args:
                username: the name of the user
                user_email: the email of the user
            Returns:
                tuple container (username, status)
        """

        failed_status = ("No-User-Given", "Failed")
        welcome_msg = """Welcome to the Iterio journey, place where users finds opportunity!

        At Iterio, we’re not just about connecting you with trusted providers; we’re handing you the keys to your path.
        Here’s how:

        1 - Your Service, Your Way: Whether you’re a dog whisperer, a coding guru, or a cupcake artist. Create your service profile, showcase your skills, and let the world know you’re open for business.
        2 - Climb the Ladder: Imagine a ladder made of opportunities. Each rung represents a service you provide. With every booking, you ascend—higher, stronger, and more confident. It’s like a game, but with real-life rewards.
        3 - Your Brand, Your Rules: No stuffy corporate policies here. You’re the boss. Set your prices, define your hours, and sprinkle your magic. Your service, your rules.

        Start Your Journey!🌟:
            1 -> Craft Your Profile: Unleash your creativity. A snazzy profile pic, a catchy bio, make it pop!
            2 -> Create Your Services: What’s your skillset? Dog walking? Logo design? Quantum mechanics? Coaching? List it all.
            3 -> Get Booked: When clients knock, open the door. Accept bookings, dazzle them, and start building your road way.

        Remember, at Iterio, you’re not just a provider; you’re a trailblazer. So grab your toolkit, and Go Conquer The Ladder of life!🚀
        """
        if not username:
            print("\n\n\t>>> No username given <<<\n")
            return failed_status
        if not user_email:
            print("\n\n\t>>> No Email Given <<<\n")
            return (username, "Fail - No email found")
        content = await connection.read_json()
        try:
            await connection.clean()
            success_count = send_mail(
                f"Welcome to Iterio {username}",
                welcome_msg,
                "iterio.supp@gmail.com",
                [user_email],
                fail_silently=False,
            )
            status, data = await connection.is_email_valid()
            if success_count > 0 and status:
                print("Email sent successfully!")
            else:
                if data == user_email:
                    print("\t###############################################################")
                    print(f"\t|\t\t\tFAILED\n\t|--->Email, send unsuccessfully to: {user_email}")
                    print("\t###############################################################")
                    content[f"{username}.{user_email}"] = {'Status': 'Invalid',
                                                           'Username': username,
                                                           'Email' : user_email,
                                                           'Filter-Method': 'User-or-Email'}
                else:
                    content[f"Last-register-user-{username}.{data}"] = {'Status': 'Undetermine-user',
                                                  'Username': f'Last-register-user-{username}',
                                                  'Email': data,
                                                  'Filter-Method': "Email"}
                await connection.save_json(content)
        except smtplib.SMTPException as e:
            print(f"FAIL sending mail:\n{e}")  
        finally:
            return (username, status)
if __name__ == '__main__':
    pass
    # UN COMMENT FOR TESTING
    #asyncio.run(connection.welcome_msg("Testing_to_find_name", "IM_INVALID@email.com"))
    #print(asyncio.run(connection.is_email_valid()))