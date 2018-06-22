import $ivy.`org.scalaj::scalaj-http:2.3.0`, scalaj.http._

val resp = Http("http://192.168.56.9:8000/internal/auth/email").headers(
  "Auth-Method" -> "plain",
  "Auth-Protocol" -> "imap",
  "Auth-Pass" -> "password",
  "Auth-Login-Attempt" -> "1",
  "Client-Host" -> "localhost",
  "Auth-User" -> "root@maildev-cmi.e-bs.cz",
  "Client-IP" -> "172.18.0.7"
)

for (index <- 1 to 100) {
  val r = resp.asString
  Console.println(s"$index: ${r.code}\n${r.headers.get("Auth-Status")} | ${r.headers.get("Auth-Wait")}\n${r.body}")
}

