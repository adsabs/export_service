import requests

class Client:
  '''The Client class is a thin wrapper around requests; Use it as a centralized place to set
  application specific parameters, such as the oauth2 authorization header'''

  def __init__(self,client_config,send_oauth2_token=True):
    self.config = client_config
    self.session = requests.Session()
    if send_oauth2_token:
      self.token = self.config['TOKEN'] #Better to raise KeyError than default to an unusable token
      self.session.headers.update({'Authorization': 'Bearer %s' % self.token})