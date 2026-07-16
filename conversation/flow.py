"""
Conversation Flow
Handles lead capture conversation using a simple state machine.
"""


class ConversationFlow:

    STATES = [
        "ASK_NAME",
        "ASK_PHONE",
        "ASK_EMAIL",
        "ASK_INTEREST",
        "FINISHED"
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reset conversation.
        """

        self.state = "ASK_NAME"

        self.user_data = {
            "name": "",
            "phone": "",
            "email": "",
            "interest": ""
        }

    def current_state(self):
        """
        Return current state.
        """

        return self.state

    def progress(self):
        """
        Return conversation progress.
        """

        completed = self.STATES.index(self.state)

        total = len(self.STATES) - 1

        return round((completed / total) * 100)

    def process_message(self, message):

        message = message.strip()

        if self.state == "ASK_NAME":

            self.user_data["name"] = message

            self.state = "ASK_PHONE"

            return {
                "reply": "Please enter your Pakistani phone number.",
                "next_state": self.state
            }

        elif self.state == "ASK_PHONE":

            self.user_data["phone"] = message

            self.state = "ASK_EMAIL"

            return {
                "reply": "Please enter your email address (or type Skip).",
                "next_state": self.state
            }

        elif self.state == "ASK_EMAIL":

            self.user_data["email"] = message

            self.state = "ASK_INTEREST"

            return {
                "reply":
                "What are you interested in?\n\n"
                "1. AI Development\n"
                "2. Web Development\n"
                "3. Mobile App\n"
                "4. Digital Marketing\n"
                "5. Internship\n"
                "6. Other",

                "next_state": self.state
            }

        elif self.state == "ASK_INTEREST":

            self.user_data["interest"] = message

            self.state = "FINISHED"

            return {
                "reply":
                "Thank you! Your information has been recorded successfully.\n"
                "Our team will contact you shortly.",

                "next_state": self.state
            }

        return {
            "reply": "Conversation already completed.",
            "next_state": "FINISHED"
        }

    def get_user_data(self):
        """
        Return collected lead information.
        """

        return self.user_data.copy()

    def is_finished(self):
        """
        Check if conversation has ended.
        """

        return self.state == "FINISHED"