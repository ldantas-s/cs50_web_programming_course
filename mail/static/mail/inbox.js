let errorMessage;
let successMessage;
const views = {
  COMPOSE_VIEW: 'compose-view',
  EMAILS_VIEW: 'emails-view',
  EMAIL_VIEW: 'email-view',
};

document.addEventListener('DOMContentLoaded', async function () {
  errorMessage = document.getElementById('compose-form-error');
  successMessage = document.getElementById('compose-form-success');

  errorMessage.style.display = 'none';
  successMessage.style.display = 'none';

  // Use buttons to toggle between views
  document
    .querySelector('#inbox')
    .addEventListener('click', () => load_mailbox('inbox'));
  document
    .querySelector('#sent')
    .addEventListener('click', () => load_mailbox('sent'));
  document
    .querySelector('#archived')
    .addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function displayView(viewId) {
  Object.values(views).forEach((view) => {
    document.querySelector(`#${view}`).style.display =
      viewId === view ? 'block' : 'none';
  });
}

function compose_email() {
  const form = document.getElementById('compose-form');

  form.addEventListener('submit', (event) => {
    const body = JSON.stringify({
      recipients: form['compose-recipients'].value,
      subject: form['compose-subject'].value,
      body: form['compose-body'].value,
    });

    fetch('/emails', {
      method: 'POST',
      body,
    }).then(async (response) => {
      const feedback = await response.json();

      if (response.status !== 201) {
        errorMessage.style.display = 'block';
        errorMessage.innerHTML = feedback.error;
        return;
      }

      errorMessage.style.display = 'none';
      successMessage.style.display = 'block';
      successMessage.innerHTML = feedback.message;
    });
  });

  // Show compose view and hide other views
  displayView(views.COMPOSE_VIEW);
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function updateMail(mailId, payload) {
  const body = JSON.stringify(payload);

  fetch(`/emails/${mailId}`, {
    method: 'PUT',
    body,
  }).then(async (response) => {
    const feedback = await response.json();

    if (response.status !== 204) {
      successMessage.style.display = 'none';
      errorMessage.style.display = 'block';
      errorMessage.innerHTML = feedback;
      return;
    }

    errorMessage.style.display = 'none';
    successMessage.style.display = 'block';
    successMessage.innerHTML = feedback;
  });
}

function createElement(elementName = 'span', props) {
  const element = document.getElementById(props.id);

  if (element) {
    // element.innerHTML = props.innerHTML;
    Object.assign(element, { ...props });
    return element;
  }

  return Object.assign(document.createElement(elementName), { ...props });
}

function getMail(id) {
  displayView(views.EMAIL_VIEW);

  updateMail(id, { read: true });

  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((data) => {
      const elements = {
        sender: createElement('span', {
          id: 'from__value',
          innerHTML: data.sender,
        }),
        recipients: createElement('span', {
          id: 'to__value',
          innerHTML: data.recipients[0],
        }),
        subject: createElement('span', {
          id: 'subject__value',
          innerHTML: data.subject,
        }),
        body: createElement('span', {
          id: 'body__value',
          innerHTML: data.body,
        }),
        timestamp: createElement('span', {
          id: 'timestamp__value',
          innerHTML: data.timestamp,
        }),
      };

      document.getElementById('email-view__from').append(elements.sender);
      document.getElementById('email-view__to').append(elements.recipients);
      document.getElementById('email-view__subject').append(elements.subject);
      document.getElementById('email-view__body').append(elements.body);
      document
        .getElementById('email-view__timestamp')
        .append(elements.timestamp);
    });
}

function getMailsbox(mailbox) {
  const mailboxList = document.getElementById('emails-view__list');

  mailboxList.innerHTML = '';

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((mails) => {
      mails.forEach((mail) => {
        const archiveButton = createElement('button', {
          className: 'btn btn-primary',
          id: `button-archive__${mail.id}`,
          innerHTML: `<i class="fa fa-archive" aria-hidden="true"></i> ${
            mail.archived ? 'Unarchive' : 'Archive'
          }`,
          onclick: (event) => {
            event.stopPropagation();
            updateMail(mail.id, { archived: !mail.archived });
            load_mailbox('inbox');
          },
        });
        const elementLi = document.createElement('li');
        const itemContent = `<div class='d-flex justify-content-between align-items-center w-75'><span><b>${mail.sender}</b> ${mail.subject}</span> <span>${mail.timestamp}</span></div>`;
        const mailStauts = mail.read ? 'list-group-item-light' : '';

        const classes = `list-group-item d-flex justify-content-between list-group-item-action ${mailStauts}`;

        Object.assign(elementLi, {
          className: classes,
          innerHTML: itemContent,
          onclick: () => getMail(mail.id),
        });
        elementLi.append(archiveButton);

        mailboxList.append(elementLi);
      });
    });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  displayView(views.EMAILS_VIEW);
  // document.querySelector('#compose-view').style.display = 'none';
  // document.querySelector('#emails-view').style.display = 'block';

  getMailsbox(mailbox);

  // Show the mailbox name
  document.querySelector('#emails-view__title').innerHTML =
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1);
}
