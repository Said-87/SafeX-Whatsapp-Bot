from flask import (
    Flask,
    request,
    jsonify,
    session,
    render_template
)
from config import (
    SECRET_KEY,
    DEBUG,
    HOST,
    PORT,
    LEAD_KEYWORDS
)

# ---------------------------------------
# Reply Engine
# ---------------------------------------

from reply_engine.matcher import FAQMatcher
from reply_engine.responses import (
    format_reply,
    welcome_message,
    goodbye_message
)

# ---------------------------------------
# Conversation
# ---------------------------------------

from conversation.flow import ConversationFlow
from conversation.lead_capture import (
    validate_name,
    validate_phone,
    validate_email
)
from conversation.crm import save_lead

# ---------------------------------------
# Support
# ---------------------------------------

from support.language import detect_language
from support.analytics import log_chat
from support.escalation import escalate_to_agent

# ---------------------------------------
# Flask App
# ---------------------------------------

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ---------------------------------------
# Objects
# ---------------------------------------

matcher = FAQMatcher()
conversation = ConversationFlow()

# ---------------------------------------
# Session Helper
# ---------------------------------------

def initialize_session():
    """
    Initialize session variables.
    """

    session.setdefault("lead_capture", False)


# ---------------------------------------
# Lead Request Detection
# ---------------------------------------

def is_lead_request(message):
    """
    Check whether the user wants to contact sales.
    """

    text = message.lower().strip()

    return any(
        keyword.lower() in text
        for keyword in LEAD_KEYWORDS
    )


# ---------------------------------------
# Home Route
# ---------------------------------------

@app.route("/", methods=["GET"])
def home():

    return render_template("index.html")
# ---------------------------------------
# Health Route
# ---------------------------------------

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


# ---------------------------------------
# Chat Route
# ---------------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    initialize_session()

    try:

        # ---------------------------------------
        # Validate Request
        # ---------------------------------------

        if not request.is_json:

            return jsonify({
                "error": "Request must be JSON."
            }), 400

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No JSON data received."
            }), 400

        message = data.get("message", "").strip()

        if not message:

            return jsonify({
                "error": "Message cannot be empty."
            }), 400

        # ---------------------------------------
        # Detect Language
        # ---------------------------------------

        language = detect_language(message)

        # ---------------------------------------
        # Continue Lead Capture
        # ---------------------------------------

        if session.get("lead_capture", False):

            state = conversation.current_state()

            # ---------------- Name ----------------

            if state == "ASK_NAME":

                if not validate_name(message):

                    return jsonify({
                        "reply": "Please enter a valid full name."
                    })

                result = conversation.process_message(message)

                return jsonify({
                    "conversation": result["reply"],
                    "state": result["next_state"],
                    "progress": conversation.progress()
                })

            # ---------------- Phone ----------------

            elif state == "ASK_PHONE":

                if not validate_phone(message):

                    return jsonify({
                        "reply": "Please enter a valid Pakistani phone number."
                    })

                result = conversation.process_message(message)

                return jsonify({
                    "conversation": result["reply"],
                    "state": result["next_state"],
                    "progress": conversation.progress()
                })

            # ---------------- Email ----------------

            elif state == "ASK_EMAIL":

                if not validate_email(message):

                    return jsonify({
                        "reply": "Please enter a valid email address or type Skip."
                    })

                result = conversation.process_message(message)

                return jsonify({
                    "conversation": result["reply"],
                    "state": result["next_state"],
                    "progress": conversation.progress()
                })

            # ---------------- Interest ----------------

            elif state == "ASK_INTEREST":

                result = conversation.process_message(message)

                user = conversation.get_user_data()

                crm_status = save_lead(
                    user["name"],
                    user["phone"],
                    user["email"],
                    user["interest"]
                )

                conversation.reset()

                session.pop("lead_capture", None)

                return jsonify({
                    "conversation": result["reply"],
                    "crm": crm_status,
                    "progress": 100
                })

        # ---------------------------------------
        # Continue in Part 3
        # ---------------------------------------

        # ---------------------------------------
        # Start Lead Capture
        # ---------------------------------------

        if is_lead_request(message):

            session["lead_capture"] = True

            conversation.reset()

            return jsonify({

                "language": language,

                "conversation":
                "Thank you for your interest.\n\n"
                "Before we connect you with our sales team, "
                "please tell me your full name.",

                "state": conversation.current_state(),

                "progress": 0

            })

        # ---------------------------------------
        # FAQ Matching
        # ---------------------------------------

        faq = matcher.get_reply(message)

        # ---------------------------------------
        # Successful Match
        # ---------------------------------------

        if faq["status"] == "success":

            log_chat(

                message,

                faq["reply"],

                "Success"

            )

            return jsonify({

                "language": language,

                "reply": format_reply(
                    faq,
                    language
                ),

                "category": faq["category"],

                "confidence": faq["confidence"]

            })

        # ---------------------------------------
        # Escalation
        # ---------------------------------------

        ticket = escalate_to_agent({

            "message": message,

            "language": language,

            "reason": "FAQ Not Found"

        })

        log_chat(

            message,

            "Escalated to Human Agent",

            "Escalated"

        )

        return jsonify({

            "language": language,

            "reply": format_reply(
                faq,
                language
            ),

            "ticket": ticket

        })

    except Exception as e:

        app.logger.exception(e)

        return jsonify({
            "error": "Internal Server Error"
        }), 500

# ---------------------------------------
# Welcome Route
# ---------------------------------------

@app.route("/welcome", methods=["GET"])
def welcome():

    language = request.args.get("language", "en")

    return jsonify({
        "reply": welcome_message(language)
    })


# ---------------------------------------
# Goodbye Route
# ---------------------------------------

@app.route("/goodbye", methods=["GET"])
def goodbye():

    language = request.args.get("language", "en")

    return jsonify({
        "reply": goodbye_message(language)
    })


# ---------------------------------------
# Error Handlers
# ---------------------------------------

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "error": "Internal Server Error."
    }), 500


# ---------------------------------------
# Run Application
# ---------------------------------------

if __name__ == "__main__":

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )

