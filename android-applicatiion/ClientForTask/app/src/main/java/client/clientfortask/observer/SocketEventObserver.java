package client.clientfortask.observer;

import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Looper;


import java.util.ArrayList;
import java.util.List;

import client.clientfortask.listener.SocketEventListener;

public class SocketEventObserver {
    private Handler handler = new Handler(Looper.getMainLooper());

    private List<SocketEventListener> socketEventListeners;
    private Context context;
    private static SocketEventObserver instance;

    private SocketEventObserver() {
        socketEventListeners = new ArrayList<>();
    }

    public void addObserve(SocketEventListener listener) {
        synchronized (socketEventListeners) {
            socketEventListeners.add(listener);
        }
    }

    public void init(Context context) {
        this.context = context;
    }

    public void removeObserve(SocketEventListener listener) {
        synchronized (socketEventListeners) {
            socketEventListeners.remove(listener);
        }
    }

    public static SocketEventObserver getInstance() {
        if (instance == null) {
            synchronized (SocketEventObserver.class) {
                if (instance == null) {
                    instance = new SocketEventObserver();
                }
            }
        }
        return instance;
    }

    public void clear(){
        synchronized (socketEventListeners) {
            socketEventListeners.clear();
        }
    }

    public void notifyReceviedData(final String data) {
        synchronized (socketEventListeners) {
            handler.post(new Runnable() {
                @Override
                public void run() {
                    for (int index = 0; index < socketEventListeners.size(); index++) {
                        socketEventListeners.get(index).socketReceviedData(data);
                    }
                }
            });
        }
    }

    public void notifyConnectObserverFailed() {
        synchronized (socketEventListeners) {
            handler.post(new Runnable() {
                @Override
                public void run() {
                    for (int index = 0; index < socketEventListeners.size(); index++) {
                        socketEventListeners.get(index).socketConnectFailed();
                    }
                }
            });
        }
    }

    public void notifyConnectObserverSuccess() {
        synchronized (socketEventListeners) {
            handler.post(new Runnable() {
                @Override
                public void run() {
                    for (int index = 0; index < socketEventListeners.size(); index++) {
                        socketEventListeners.get(index).socketConnectSuccess();
                    }
                }
            });
        }
    }
}
