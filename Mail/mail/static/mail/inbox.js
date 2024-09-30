document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(reply = null) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-open').style.display = 'none';

  // Clear out composition fields
  if (reply['recipients'] == undefined){
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    document.querySelector('#compose-recipients').value = reply['recipients'];
    document.querySelector('#compose-subject').value = reply['subject'];
    document.querySelector('#compose-body').value = reply['body'];
  }

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-open').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    email.forEach(obj => {
        const newEmail = document.createElement('div');
        newEmail.id = 'newEmail';
        newEmail.innerHTML = `<span id='emailSender'>${obj.recipients}</span> <span id='emailSubject'>${obj.subject}</span> <span id='emailTimestamp'>${obj.timestamp}</span>`;
        newEmail.addEventListener('click', function() {
          console.log('This element has been clicked!');
          open_email(obj.id, mailbox);
        });
        if (obj.read && mailbox != 'sent') {
          newEmail.style.background = 'rgb(220, 220, 220)';
        }
        document.querySelector('#emails-view').append(newEmail);
    });
  });
}

function send_email(event) {
  event.preventDefault();

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);

    if (result.message === "Email sent successfully.") {
      load_mailbox('sent');
    } else {
      alert(result.error);
    }
  });
}

function open_email(email_id, mailbox) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-open').style.display = 'block';


  document.querySelector('#emails-open').innerHTML = '';

  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    const viewEmail = document.createElement('div');
    viewEmail.id = 'viewEmail';
    viewEmail.innerHTML = `<div id='viewTop'><span id='viewFrom'><span id='fromTo'>From: </span>${email.sender}</span> <span id='viewTimestamp'>${email.timestamp}</span></div> <div id='viewTo'><span id='fromTo'>To: </span>${email.recipients}</div>
    <div id='viewSubject'>${email.subject}</div><div id='viewBody'>${email.body}</div>`;

    document.querySelector('#emails-open').append(viewEmail);

    const viewButtons = document.createElement('div');
    viewButtons.id = 'viewButtons';
    let archiveMsg;
    if (mailbox === "inbox") {
      archiveMsg = 'Archive';
    } else {
      archiveMsg = 'Unarchive';
    }

    if (mailbox != 'sent') {
      viewButtons.innerHTML = `<button id='viewReply'>Reply</button><button id='viewArchive'>${archiveMsg}</button>`;

    document.querySelector('#emails-open').append(viewButtons);

    const replyButton = document.getElementById('viewReply');
    const archiveButton = document.getElementById('viewArchive');

    replyButton.addEventListener('click', function() {
      console.log('Reply has been clicked!');
      var replyDetails = {
        'recipients': email.sender,
        'subject': (email.subject).substring(0, 3) == 'Re:' ? `${email.subject}` : `Re: ${email.subject}`,
        'body': `On ${email.timestamp} ${email.sender} wrote: ${email.body}`
      };
      compose_email(replyDetails)
    });

    archiveButton.addEventListener('click', function() {
      console.log('Archive has been clicked!');
      fetch(`emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: email.archived ? false : true
        })
      })
      .then(() => {
        load_mailbox('inbox');
      })
    });
    };

    });

    fetch(`emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
}