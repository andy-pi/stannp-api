import requests
import base64

class StannpClient():

    def __init__( self, api_key ):
        self.api_key = api_key

    def perform_request( self, endpoint_url, payload, files, typeofr):
        '''
        Performs a generic API request and returns the JSON response
        '''
        if (typeofr == "get"): r = requests.get( endpoint_url), auth=(self.api_key,"") )
        if (typeofr == "post"): r = requests.post( endpoint_url, data=payload, files=files, auth=(self.api_key,""))
        print r.request.headers
        return r.json()

    def get_balance( self ):
        '''
        Returns the Stannp Account balance in JSON format
        '''
        return self.perform_request( "https://dash.stannp.com/api/v1/accounts/balance", typeofr="get", files=None, payload=None)
        
    def list_campaigns(self):
        '''
        Returns a list of campaigns in JSON format
        '''
        return self.perform_request("https://dash.stannp.com/api/v1/campaigns/list", typeofr="get", files=None, payload=None)

    def get_campaign(self, campaign_id):
        '''
        Returns a the specified campaign in JSON format
        '''
        payload={}
        payload['id']=campaign_id
        return self.perform_request("https://dash.stannp.com/api/v1/campaigns/get/",  payload=payload, files=None, typeofr="post")
        
    def delete_campaign(self, campaign_id):
        '''
        ? NOT WORKING
        Deletes a the specified campaign and returns a message
        '''
        payload={}
        payload['id']=campaign_id
        return self.perform_request("https://dash.stannp.com/api/v1/campaigns/delete", payload=payload, files=None, typeofr="post")
        
    def new_campaign(self, name, typeofc, code):
        '''
        Creates a new campaign give a name, and type of campaign, from the following:
        a6-postcard | a5-postcard | dl-postcard | letter-dl 
        '''
        payload={}
        payload['name']=name
        payload['type']=typeofc
        payload['code']=code
        return self.perform_request("https://dash.stannp.com/api/v1/campaigns/draft", payload, files=None, typeofr="post")
    
    def get_groups(self):
        '''
        Returns a list of recipient groups in JSON format
        '''
        return self.perform_request("https://dash.stannp.com/api/v1/groups/list", typeofr="get", files=None, payload=None)
   
    def new_group(self, name):
        '''
        Creates a new recipient group with the specified name, with the result returned in JSON format
        '''
        payload={}
        payload['name']=name
        return self.perform_request("https://dash.stannp.com/api/v1/groups/new", typeofr="post", files=None, payload=payload)
        
    def validate_address(self, address):
        '''
        ? NOT WORKING
        company 	string 	Company name
        address1 	string 	Address line 1
        address2 	string 	Address line 2
        address3 	string 	Address line 3
        city 	    string 	Address city
        postcode 	string 	Address postal code
        country 	string 	ISO 3166-1 Alpha 2 Country Code (GB,US,FR...)
        '''
        return self.perform_request("https://dash.stannp.com/api/v1/recipients/validate", payload, files=None, typeofr="post")
        
    def new_recipient(self, group_id, on_duplicate, recipient):
        '''
        group_id 	    int 	The group ID you wish to add the data to.
        on_duplicate 	string 	What to do if a duplicate is found (update/ignore/duplicate)
        firstname   	string 	Recipients first name
        lasttname   	string 	Recipients last name
        address1    	string 	Address line 1
        address2    	string 	Address line 2
        city        	string 	Address city
        postcode    	string 	Address postal code
        country     	string 	ISO 3166-1 Alpha 2 Country Code (GB,US,FR...)
        ? 	            ? 	    If you have added custom fields to your recipients you can also add them as parameters when added new recipient records
        
        The API will return a response to say if the request was successful or not. If successful the new recipients ID will be returned along with whether the address can be validated or not. 
        '''
        payload={}
        payload['title']=recipient['title']
        payload['firstname']=recipient['firstname']
        payload['lastname']=recipient['lastname']
        payload['address1']=recipient['address1']
        payload['address2']=recipient['address2']
        payload['city']=recipient['city']
        payload['postcode']=recipient['postcode']
        payload['country']=recipient['country']
        payload['group_id']=group_id
        payload['on_duplicate']=on_duplicate
        print payload
        return self.perform_request("https://dash.stannp.com/api/v1/recipients/new", payload, files=None, typeofr="post")

    def list_recipients(self):
        '''
        Returns a list of all recipients in JSON format
        '''
        return self.perform_request("https://dash.stannp.com/api/v1/recipients/list",payload=None, files=None, typeofr="get")
        
        
    def get_recipient(self, id):
        '''
        ? NOT WORKING
        Returns the recipient specified in JSON format
        '''
        address="https://dash.stannp.com/api/v1/recipient/get/" + str(id) + "?api_key=" + self.api_key
        print address
        return self.perform_request(address, payload=None, files=None, typeofr="get")
        
    def delete_recipient(self, id):
        '''
        Deletes the recipient specified
        '''
        payload={}
        payload['id']=id
        return self.perform_request("https://dash.stannp.com/api/v1/recipients/delete", payload, files=None, typeofr="post")

    def send_postcard(self, size, test, recipient, front, back, message, signature):
        '''
        size        mandatory 	Either "A5" or "A6"
        test 	    optional 	If test is set to true then a sample PDF file will be produced but the item will never be dispatched and no charge will be taken.
        recipient 	mandatory 	Either an ID of an existing recipient or a new recipient array.
        front 	    mandatory 	An image for the front. This can be either a URL, a file or a base64 encoded string. Supported file types are JPG or PDF
        back 	    optional 	An image for the back. This can be either a URL, a file or a base64 encoded string. Supported file types are JPG or PDF
        message 	optional 	A message on the back of the card. If using a back image this message will be overlaid on top
        signature   optional    An image which will be placed in the signature location. The image can be either a URL or a file or a base64 encoded string. This must be a JPG file with a 768 x 118 pixels resolution
        '''
        
        payload={}
        payload=self.add_recipient_to_payload(recipient)
        payload['size']=size
        payload['test']=test
        payload['message']=message
        payload['front'] = self.base64_encode_file(front)
        if back is not None: payload['back'] = self.base64_encode_file(back)
        if signature is not None: payload['signature'] = self.base64_encode_file(signature)
        
        return self.perform_request( "https://dash.stannp.com/api/v1/postcards/create", payload, files=None, typeofr="post")
        
        
    def send_letter(self, test, template, recipient, background, pages, pdforhtml):
        '''
        ? NOT WORKING WITH PDF FILES
        test        optional	If test is set to true then a sample PDF file will be produced but the item will never be dispatched and no charge will be taken.
        template 	optional 	An ID of a template already set up on the platform.
        recipient 	mandatory 	Either an ID of an existing recipient or a new recipient array.
        background 	optional 	A letter heading design or a file for the background of every page. This can be either a URL, a file or a base64 encoded string. Supported file types are JPG or PDF.
        pages 	    optional 	The text content for each page of the letter. This can be a string containing basic HTML or a PDF file. Each page can be separated by sending an array for example: pages[0]="page 1"&pages[1]="page 2". However PDF files with multiple pages will be recognised. This value is not required if a template is being used. 
        '''
        
        payload={}
        if pdforhtml=="pdf":
            files= {'pages': open(pages, 'rb')}
        else:
            payload['pages']=pages

        #payload['pages']= {'pages': open(pages, 'rb')}
        
        payload=self.add_recipient_to_payload(recipient)
        payload['test']=test
        if background is not None: payload['background'] = self.base64_encode_file(background)
        if template is not None: payload['template']=template
        #print payload
        
        return self.perform_request( "https://dash.stannp.com/api/v1/letters/create", payload, files=files, typeofr="post")
        
        
    def add_recipient_to_payload(self, recipient):
        payload={}
        payload['recipient[title]']=recipient['title']
        payload['recipient[firstname]']=recipient['firstname']
        payload['recipient[lastname]']=recipient['lastname']
        payload['recipient[address1]']=recipient['address1']
        payload['recipient[address2]']=recipient['address2']
        payload['recipient[city]']=recipient['city']
        payload['recipient[postcode]']=recipient['postcode']
        payload['recipient[country]']='GB'
        
        return payload
        
    def base64_encode_file(self, filepath):
        file = open(filepath, 'r')
        try:
            encoded_file = base64.b64encode( file.read() )
            return encoded_file
        except Exception, e:
            raise e
