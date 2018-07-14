package client.clientfortask.manager;


import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;

import client.clientfortask.observer.SocketEventObserver;
import client.clientfortask.service.ClientService;

public class ClientTask implements Runnable {
    private String host;
    private int port;
    private Socket socket;
    private InputStream inputStream;
    private PrintWriter outputStream;
    private boolean isRunning;

    public ClientTask(String host, int port) {
        this.host = host;
        this.port = port;
        isRunning = true;
    }

    @Override
    public void run() {
        try {
            System.out.println("start connect the server " + host + ":" + port);
            socket = new Socket();
            socket.connect(new InetSocketAddress(host, port), 3000);
            inputStream = socket.getInputStream();
            outputStream = new PrintWriter(socket.getOutputStream());
            SocketEventObserver.getInstance().notifyConnectObserverSuccess();
            while (isRunning && socket.isConnected()) {
                Thread.sleep(100);
                byte[] data = new byte[1024];
                int length = inputStream.read(data, 0, data.length);
                String s = new String(data, 0, length, "utf-8");
                System.out.println("the receive is " + s + " and length is " + length+" the thread is "+Thread.currentThread());
                SocketEventObserver.getInstance().notifyReceviedData(s);
            }
        } catch (IOException e) {
            SocketEventObserver.getInstance().notifyConnectObserverFailed();
            e.printStackTrace();
            socket = null;
        } catch (InterruptedException e) {
            e.printStackTrace();
            SocketEventObserver.getInstance().notifyConnectObserverFailed();
            socket = null;
        }
    }

    public void sendData(final String data) {
        if (socket != null && socket.isConnected()) {
            new Thread() {
                @Override
                public void run() {
                    System.out.println("send the data is " + data);
                    outputStream.write(data);
                    outputStream.flush();
                }
            }.start();
        }
    }

    public void stop() {
        try {
            isRunning = false;
            inputStream.close();
            outputStream.close();
            socket.close();
            outputStream = null;
            inputStream = null;
            socket = null;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
