/*
* Copyright (C) 2005 onwards University of Deusto
* All rights reserved.
*
* This software is licensed as described in the file COPYING, which
* you should have received as part of this distribution.
*
* This software consists of contributions made by many individuals, 
* listed below:
*
* Author: Pablo Orduña <pablo@ordunya.com>
*
*/ 
package es.deusto.weblab.client.comm.exceptions.login;

import es.deusto.weblab.client.comm.exceptions.WebLabServerException;

public class LoginException extends WebLabServerException {
	private static final long serialVersionUID = 6192080708862297588L;

	public LoginException() {}

	public LoginException(String arg0) {
		super(arg0);
	}

	public LoginException(Throwable arg0) {
		super(arg0);
	}

	public LoginException(String arg0, Throwable arg1) {
		super(arg0, arg1);
	}

}
