document.body.addEventListener('htmx:afterRequest', function (event) {
  if (event.detail.successful) return
  const formHandlerMapper = {
    'signup-form': signUpHandler,
    'signin-form': signInHandler,
  }
  console.log('Response received for:', event.detail);
  console.log('Response headers:', event.target.id);
  const form = event.target;
  formHandlerMapper[form.id](form);
});


const signUpHandler = (form) => {
  const userNameField = form.querySelector('input[name="username"]');
  const emailField = form.querySelector('input[name="email"]');
}

const signInHandler = () => {

}