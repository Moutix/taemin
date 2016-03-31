import smtplib

from taemin import schema, conf
from schema import Mail 
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
import email, re, requests

class Mailage:
    def __init__(self, bot):
        self.bot = bot
        self.hmtlmsg = """"""
        self.plainText = ""
        self.set_email()

    def mailage(self, chan, content, user):
        email = self.get_email(user, chan)
        if not email:
            self.bot.connection.privmsg(chan, "L'utilisateur %s n'a pas configuré d'adresse mail" % user.name)
            return

        msg = MIMEMultipart('alternative')
        self.plainText = "Bonjour, \n Ceci est un mail du plus bot du monde : Taemin\n"
        self.htmlmsg = """\
                <html>
                    <head></head>
                    <body>
                        <div><p>Bonjour ! <br>
                        Ceci est un mail du plus bot du monde : Taemin.<br>
                        </p></div>
                """

        msg['Subject'] = "Sauvegarde IRC"
        msg['From'] = "taemin@lee.ko"
        self.parsage(content, msg)

        self.htmlmsg += """</body> 
                    </html>"""
        self.sendage(email, msg)

    def parsage(self, content, msg):
        for line in content:
            if line.startswith("http"):
                self.guesstype(line)
                continue
            self.htmlmsg += """<p>"""+ line + """</p>"""
            self.plainText += line

    def guesstype(self, location):
        try:
            r = requests.get(location)
        except requests.exceptions.RequestException:
            self.htmlmsg += """<p><a href ='""" + location + """'/> </p>"""
            self.plainText += location
 
            return "<lien>%s" % location

        if r.headers["content-type"] and r.headers["content-type"].split("/")[0] == "image":
            self.htmlmsg += """<p><img src = '""" + r.url +"""'/> </p>"""
            self.plainText += r.url
      
        self.htmlmsg += """<p><a href ='""" + r.url+ """"/> </p>"""
        self.plainText += r.url


    def sendage(self, email, msg):
        part1 = MIMEText(self.plainText.encode('utf-8'), 'plain', 'utf-8')
        part2 = MIMEText(self.htmlmsg.encode('utf-8'), 'html', 'utf-8')

        msg['To'] = email
        msg.attach(part1)
        msg.attach(part2)

        mail_conf = self.bot.conf.get("Mail_conf", {})
        port = mail_conf.get("port",25)
        server = mail_conf.get("server", "localhost")

        s = smtplib.SMTP(server, port)
        s.sendmail("taemin@lee.ko", email, msg.as_string())
        s.quit()

    def get_email(self, user, chan):
        try:
            res = Mail.get(schema.Mail.user == user)
            return res.mail
        except schema.Mail.DoesNotExist:
            return None

    def set_email(self):
        delete = Mail.delete()
        delete.execute()
        for pseudo, mail in self.bot.conf.get("mails", {}).iteritems():
            user = self.get_user(pseudo)
            Mail.create(user=user, mail=mail)
        return

    def get_user(self, name):
        try:
            return schema.User.get(schema.User.name % name)
        except schema.User.DoesNotExist:
            #Il faudrait que je loggue un truc la quand meme...
            return None
