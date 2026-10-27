const turnstileDiv = document.getElementById("turnstileContainer");
const turnstileSiteKey = turnstileDiv.dataset.sitekey;

function onTurnstileLoad() {
  turnstile.render("#turnstileContainer", {
    sitekey: turnstileSiteKey,
    callback: async (token) => {
      const res = await fetch("/toavif/verify", {
        method: "POST",
        body: new URLSearchParams({ token }),
      });

      if (!res.ok) {
        return;
      }

      const { session_token } = await res.json();
      sessionStorage.setItem("session_token", session_token);

      document.getElementById("turnstileContainer").style.display = "none";
    },
  });
}
