from requests import post

class KeycloakAuthentication():

    def set_configuration(self, realm: str, client_id: str, client_secret: str, username: str, password: str, host: str, verify_ssl: bool = True):
        """This class is the object that contains the Keycloak configuration for authentication
            All params must be configured through the Keycloak server before using
            to authenticate with Koverse.

            :param str realm: Keycloak authentication URL including host and realm
            :param str client_id: Keycloak Client ID
            :param str client_secret: Keycloak Client Secret
            :param str username: Username
            :param str password: password
            :param str host: host name of keycloak service
            :param bool verify_ssl: should the certificate be verified

        """

        if realm is None:
            print("Keycloak Realm is required.")

        self.username = username
        self.password = password
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host
        self.realm = realm

        self.verify_ssl = verify_ssl

        # url = f"https://{host}/"

        # Configure client - keycloak python client defaults to grant_type password and scope openid
        # self.keycloak_openid = KeycloakOpenID(server_url=url,
        #                          client_id=client_id,
        #                          realm_name=realm,
        #                          client_secret_key=client_secret)

        # self.keycloak_openid.connection.verify = verify_ssl


    def get_keycloak_token(self) -> str:
        request_headers = {
         'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        request_body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password,
            'grant_type': 'client_credentials',
            'scope': 'openid'
        }

        return 'Bearer ' + post(f'https://{self.host}/realms/{self.realm}/protocol/openid-connect/token', headers=request_headers, data=request_body, verify=self.verify_ssl).json()['access_token']
        # return self.keycloak_openid.token(username=self.username, password=self.password)['access_token']
