/* ==========================================
   SafeX WhatsApp Business Bot
========================================== */

// ------------------------------------------
// Elements
// ------------------------------------------

const pages = document.querySelectorAll(".page");
const navButtons = document.querySelectorAll(".nav-btn");

const chatBox = document.getElementById("chatBox");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const typing = document.getElementById("typing");

const totalChats = document.getElementById("totalChats");
const successfulReplies = document.getElementById("successfulReplies");
const escalatedChats = document.getElementById("escalatedChats");
const leadCount = document.getElementById("leadCount");
const leadTable = document.getElementById("leadTable");

const themeBtn = document.getElementById("themeBtn");
const clearChatBtn = document.getElementById("clearChatBtn");

// ------------------------------------------
// Navigation
// ------------------------------------------

navButtons.forEach(button => {

    button.addEventListener("click", () => {

        navButtons.forEach(btn => btn.classList.remove("active"));

        pages.forEach(page => page.classList.remove("active"));

        button.classList.add("active");

        const page = document.getElementById(button.dataset.page);

        page.classList.add("active");

        if(button.dataset.page==="analytics"){

            loadAnalytics();

        }

        if(button.dataset.page==="leads"){

            loadLeads();

        }

    });

});

// ------------------------------------------
// Current Time
// ------------------------------------------

function getTime(){

    const now = new Date();

    return now.toLocaleTimeString([],{

        hour:"2-digit",

        minute:"2-digit"

    });

}

// ------------------------------------------
// Scroll
// ------------------------------------------

function scrollBottom(){

    chatBox.scrollTop = chatBox.scrollHeight;

}

// ------------------------------------------
// Messages
// ------------------------------------------

function addUserMessage(text){

    const message = document.createElement("div");

    message.className = "message user";

    message.innerHTML = `
        ${text}
        <br>
        <small>${getTime()}</small>
    `;

    chatBox.appendChild(message);

    scrollBottom();

}

function addBotMessage(text){

    const message = document.createElement("div");

    message.className = "message bot";

    message.innerHTML = `
        ${text}
        <br>
        <small>${getTime()}</small>
    `;

    chatBox.appendChild(message);

    scrollBottom();

}

// ------------------------------------------
// Typing
// ------------------------------------------

function showTyping(){

    typing.style.display="flex";

}

function hideTyping(){

    typing.style.display="none";

}

// ------------------------------------------
// Send Message
// ------------------------------------------

async function sendMessage(){

    const message=input.value.trim();

    if(message==="") return;

    addUserMessage(message);

    input.value="";

    showTyping();

    sendBtn.disabled=true;

    try{

        const response=await fetch("/chat",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                message:message

            })

        });

        const data=await response.json();

        hideTyping();

        sendBtn.disabled=false;

        if(data.reply){

            addBotMessage(data.reply);

        }

        else if(data.conversation){

            addBotMessage(data.conversation);

        }

        else if(data.error){

            addBotMessage("❌ "+data.error);

        }

        else{

            addBotMessage("Unexpected response received.");

        }

    }

    catch(error){

        hideTyping();

        sendBtn.disabled=false;

        addBotMessage("⚠ Unable to connect to the server.");

        console.error(error);

    }

}

// ------------------------------------------
// Send Button
// ------------------------------------------

sendBtn.addEventListener("click",sendMessage);

input.addEventListener("keydown",function(e){

    if(e.key==="Enter"){

        sendMessage();

    }

});

// ------------------------------------------
// Analytics
// ------------------------------------------

async function loadAnalytics(){

    try{

        const response=await fetch("/analytics");

        const data=await response.json();

        totalChats.textContent=data.total_chats;

        successfulReplies.textContent=data.successful_replies;

        escalatedChats.textContent=data.escalated_chats;

        leadCount.textContent=data.leads || 0;

    }

    catch(error){

        console.error(error);

    }

}

// ------------------------------------------
// Leads
// ------------------------------------------

async function loadLeads(){

    try{

        const response=await fetch("/leads");

        const leads=await response.json();

        leadTable.innerHTML="";

        if(leads.length===0){

            leadTable.innerHTML=`
                <tr>
                    <td colspan="4">
                        No Leads Found
                    </td>
                </tr>
            `;

            return;

        }

        leads.forEach(lead=>{

            leadTable.innerHTML+=`

                <tr>

                    <td>${lead.name}</td>

                    <td>${lead.phone}</td>

                    <td>${lead.email}</td>

                    <td>${lead.interest}</td>

                </tr>

            `;

        });

    }

    catch(error){

        console.error(error);

    }

}

// ------------------------------------------
// Dark Mode
// ------------------------------------------

themeBtn.addEventListener("click",()=>{

    document.body.classList.toggle("dark");

});

// ------------------------------------------
// Clear Chat
// ------------------------------------------

clearChatBtn.addEventListener("click",()=>{

    chatBox.innerHTML=`

        <div class="message bot">

            Chat cleared.

        </div>

    `;

});

// ------------------------------------------
// Startup
// ------------------------------------------

window.onload=()=>{

    input.focus();

};