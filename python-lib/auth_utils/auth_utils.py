def get_jwt(preset, kdp_conn, logger):

    jwt = preset.get("kdp_jwt")
    auth_type = preset.get("auth_type")

    if auth_type == "basic_login":
        logger.info('auth type is basic_login, perform authentication using email and password')

        email = preset.get("email")
        password = preset.get("password")
        workspace_id = preset.get("workspace_id")

        if email is None or password is None:
            raise ValueError("Please provide email address and password in the preset")

        authentication_details = kdp_conn.create_authentication_token(email=email, password=password,
                                                                      workspace_id=workspace_id)
        jwt = authentication_details.get("access_token")

        logger.info('jwt has been created')

    elif auth_type == "keycloak_login":
        logger.info('auth type is keycloak_login, perform authentication using keycloak')

        keycloak_host = preset.get("keycloak_host")
        keycloak_realm = preset.get("keycloak_realm")
        keycloak_client_id = preset.get("keycloak_client_id")
        keycloak_client_secret = preset.get("keycloak_client_secret")
        keycloak_username = preset.get("keycloak_username")
        keycloak_password = preset.get("keycloak_password")
        workspace_id = preset.get("workspace_id")

        authentication_details = kdp_conn.create_keycloak_authentication_token(username=keycloak_username,
                                                                       realm=keycloak_realm,
                                                                       client_id=keycloak_client_id,
                                                                       client_secret=keycloak_client_secret,
                                                                       password=keycloak_password,
                                                                       workspace_id=workspace_id,
                                                                       host=keycloak_host,
                                                                       verify_ssl=False)
        jwt = authentication_details.get("access_token")

        logger.info('jwt has been created via keycloak')

    else:
        if jwt is None or jwt == "":
            raise ValueError("Please provide KDP JSON Web Token in the preset")

        logger.info('jwt is provided in the preset')

    return jwt
