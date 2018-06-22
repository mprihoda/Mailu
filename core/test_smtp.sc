import java.util.UUID

import $ivy.`org.apache.commons:commons-email:1.5`
import org.apache.commons.mail._

val batch = UUID.randomUUID().toString

def email(index: Int) = {
  val e = new SimpleEmail()
  e.setHostName("mailtest-cmi.e-bs.cz")
  e.setSmtpPort(465)
  e.setSSLOnConnect(true)
  e.setAuthentication("root@mailtest-cmi.e-bs.cz", "howtoget")
  e.setFrom("root@mailtest-cmi.e-bs.cz")
  e.setSubject(s"Perf test email $index [$batch]")
  e.setMsg("This is a test mail")
  e.addTo("admin@mailtest-cmi.e-bs.cz")
  e
}

for (index <- 1 to 20) {
  email(index).send()
}
