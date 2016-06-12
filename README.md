# A Python API wrapper for Stannp by AndyPi

## What is Stannp?
Stannp allows you to send snail mail via a web api. It includes postcards and letters. See stannp.com for more details.  

## Installation
No dependencies - just clone the repo:  
```
git clone https://github.com/andy-pi/stannp-api.git
```  

# Example Usage

## Initiatalisation
import the module and create an instance with your Stannp API Key  
```
from stannp import StannpClient
STANNP_API_KEY="XXXXXXXXXXXX"
stannpinstance=StannpClient(STANNP_API_KEY)
```

## Test send a postcard and return the JSON repsonse
```
# set recipient using a python dictionary
recipient={'title': 'Mr', 'firstname':'Andy', 'lastname':'Pi', 'address1': 'My House', 'address2': 'My Town', 'city':My City', 'postcode': 'Postcode', 'country':'GB'} 	
# Set the message text
message="Hi Friend,\n\n This is a sample postcard using AndyPi's stannp-api wrapper for python"
# Creates the postcard (where test.jpg is the filename of the front of the card)
card=stannpinstance.send_postcard(size="A6", test=True, recipient=recipient, front="test.jpg", back=None, message=message, signature=None)
# Prints the JSON repsonse from the stannp server, including the URL of a PDF preview
print card

```

## Test send a letter and return the PDF preview URL from the repsonse
```
# set recipient using a python dictionary
recipient={'title': 'Mr', 'firstname':'Andy', 'lastname':'Pi', 'address1': 'My House', 'address2': 'My Town', 'city':My City', 'postcode': 'Postcode', 'country':'GB'} 	
# Set the message text to be a PDF named test.pdf (note the first page will have the recipients address)
letter=stannpinstance.send_letter(test=True, template=None, recipient=recipient, background=None, pages="test.pdf", pdforhtml="pdf")
# print the URL of the preview PDF
print letter['data']['pdf']
```

## Other
Please see the comments / doctrings in stannp.py to understand how to use all the functions.
