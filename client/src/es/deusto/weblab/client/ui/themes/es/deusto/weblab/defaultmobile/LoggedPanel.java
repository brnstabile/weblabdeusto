/*
* Copyright (C) 2005-2009 University of Deusto
* All rights reserved.
*
* This software is licensed as described in the file COPYING, which
* you should have received as part of this distribution.
*
* This software consists of contributions made by many individuals, 
* listed below:
*
* Author: FILLME
*
*/

package es.deusto.weblab.client.ui.themes.es.deusto.weblab.defaultmobile;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.uibinder.client.UiHandler;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.Widget;

import es.deusto.weblab.client.dto.users.User;
import es.deusto.weblab.client.ui.themes.es.deusto.weblab.defaultmobile.i18n.IWebLabDeustoThemeMessages;
import es.deusto.weblab.client.ui.widgets.WlUtil;
import es.deusto.weblab.client.ui.widgets.WlVerticalPanel;

class LoggedPanel extends Composite {
	
    // i18n
    private IWebLabDeustoThemeMessages i18nMessages = (IWebLabDeustoThemeMessages)
    	GWT.create(IWebLabDeustoThemeMessages.class);
    	
    interface ILoggedPanelCallback {
    	public void onLogoutButtonClicked();
    }
    
	interface LoggedPanelUiBinder extends UiBinder<Widget, LoggedPanel> {
	}

	private static LoggedPanelUiBinder uiBinder = GWT.create(LoggedPanelUiBinder.class);
    
	// Widgets
    @UiField WlVerticalPanel contentPanel;  
    @UiField Label userLabel;
	@UiField Anchor logoutLink;
	
	// DTOs
	private final User user;
    private ILoggedPanelCallback callback;
	
    LoggedPanel(User user, ILoggedPanelCallback callback) {
		this.user = user;
		this.callback = callback;
	
	    final Widget wid = uiBinder.createAndBindUi(this);
	    this.initWidget(wid);

		this.userLabel.setText(WlUtil.escapeNotQuote(this.user.getFullName()));
		this.logoutLink.setText(this.i18nMessages.logOut());
	}

	@UiHandler("logoutLink")
	void onLogoutClicked(@SuppressWarnings("unused") ClickEvent ev) {
		System.out.println("Logout button clicked.");
		this.callback.onLogoutButtonClicked();
	}
	
}
