const params = new URLSearchParams(location.search);

const username = params.get("username");

if (!username) {
    document.body.innerHTML = "username required";
    throw new Error("username required");
}

function glow(color) {
    return `
        0 0 1px ${color},
        0 0 2px ${color},
        0 0 2px rgba(0,0,0,.45)
    `;
}

const chat = document.getElementById("chat");

const source = new EventSource(`/events?username=${encodeURIComponent(username)}`);

const MAX_MESSAGES = 30;

source.onmessage = ({ data }) => {

    const msg = JSON.parse(data);

    const row = document.createElement("div");
    row.className = "message";

    if (msg.loud_voice) {
        row.classList.add("loud");
    }

    const department = document.createElement("span");
    department.className = "department";
    department.style.color = msg.department_color;
    department.style.textShadow = glow(msg.department_color);
    department.textContent = `[${msg.department}] `;

    const badgeBox = document.createElement("span");
    badgeBox.className = "badges";


    for (const badge of msg.badges) {

        const img = document.createElement("img");

        img.className = "badge";

        img.src =
            `https://static-cdn.jtvnw.net/badges/v1/${badge.name}/${badge.version}/1`;

        badgeBox.append(img);
    }

    const nick = document.createElement("span");
    nick.className = "nick";
    nick.style.color = msg.color;
    nick.style.textShadow = glow(msg.color);
    nick.textContent = msg.display_name;

    const speech = document.createElement("span");
    speech.className = "speech";
    speech.style.color = msg.department_color;
    speech.style.textShadow = glow(msg.department_color);
    speech.textContent = ` ${msg.speech}, `;

    const text = document.createElement("span");
    text.className = "text";
    text.style.color = msg.department_color;
    text.style.textShadow = glow(msg.department_color);
    function renderEmotes(text, emotes){

    if(!emotes.length)
        return document.createTextNode(`"${text}"`);


    let parts = [];
    let last = 0;


    for(const e of emotes){

        parts.push(
            document.createTextNode(
                text.substring(last,e.start)
            )
        );


        const img=document.createElement("img");

        img.className="emote";

        img.src =
        `https://static-cdn.jtvnw.net/emoticons/v2/${e.id}/default/dark/1.0`;


        parts.push(img);

        last=e.end+1;
    }


    parts.push(
        document.createTextNode(
            text.substring(last)
        )
    );


    const span=document.createElement("span");

    span.append(...parts);

    return span;
}
    text.append(
    document.createTextNode('"'),
    renderEmotes(msg.text,msg.emotes),
    document.createTextNode('"')
);

    row.append(
        badgeBox,
        department,
        nick,
        speech,
        text
);

    chat.append(row);

    while (chat.children.length > MAX_MESSAGES) {
        chat.firstChild.remove();
    }

};