package client.clientfortask.application;

import android.app.Application;

import client.clientfortask.observer.SocketEventObserver;
import client.clientfortask.service.ClientService;

public class ClientApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        SocketEventObserver.getInstance().init(this);
    }
}
