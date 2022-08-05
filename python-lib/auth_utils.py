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
    else:
        if jwt is None or jwt == "":
            raise ValueError("Please provide KDP JSON Web Token in the preset")

        logger.info('jwt is provided in the preset')

    return jwt
