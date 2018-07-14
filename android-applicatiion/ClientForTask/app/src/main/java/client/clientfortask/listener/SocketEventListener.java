package client.clientfortask.listener;

public interface SocketEventListener {
    void socketConnectSuccess();
    void socketConnectFailed();
    void socketReceviedData(String s);
}
