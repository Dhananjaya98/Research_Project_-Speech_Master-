
var firebaseConfig = {
  apiKey: "AIzaSyBhnLZA8NKFBEOojrjK27sVVO_z6H1EDKE",
  authDomain: "speech-master-login.firebaseapp.com",
  projectId: "speech-master-login",
  storageBucket: "speech-master-login.appspot.com",
  messagingSenderId: "1055856699477",
  appId: "1:1055856699477:web:cd5cc6c7e341000a828cdc",
  measurementId: "G-L8DLH18DG8"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();

//signup function
function signUp() {
  var email = document.getElementById("email");
  var password = document.getElementById("password");

  const promise = auth.createUserWithEmailAndPassword(email.value, password.value);
  promise.catch(e => alert(e.message));
  alert("SignUp Successfully");
}

//signIN function
function signIn() {
  var email = document.getElementById("email");
  var password = document.getElementById("password");
  const promise = auth.signInWithEmailAndPassword(email.value, password.value);
  promise.catch(e => alert(e.message));
  //    alert("SignUp In Successfully");
}


//signOut
function signOut() {
  auth.signOut();
  alert("SignOut Successfully from System");
}

//active user to homepage
firebase.auth().onAuthStateChanged((user) => {
  if (user) {
    var email = user.email;
    alert("Active user " + email);

  } else {
    alert("No Active user Found")
  }
})