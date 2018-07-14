package client.clientfortask.activity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import client.clientfortask.R;
import client.clientfortask.listener.SimpleSocketEventListener;
import client.clientfortask.manager.ClientManager;
import client.clientfortask.obj.ServerInfo;
import client.clientfortask.obj.ServerInitObj;
import client.clientfortask.observer.SocketEventObserver;
import client.clientfortask.service.ClientService;
import client.clientfortask.utils.SharePreferenceUtils;

public class MainActivity extends BaseActivity implements View.OnClickListener {
    private EditText ip;
    private EditText port;
    private Button connect;
    private ProgressDialog dialog;
    private SimpleSocketEventListener listener = new SimpleSocketEventListener() {
        @Override
        public void socketConnectFailed() {
            dialog.dismiss();
            Toast.makeText(MainActivity.this, "connect failed ", Toast.LENGTH_SHORT).show();
        }

        @Override
        public void socketReceviedData(String s) {
            super.socketReceviedData(s);
            try {
                JSONObject object = new JSONObject(s);
                if (object.getString("command").equals("Server isn't initialized")) {
                    Intent intent = new Intent(MainActivity.this, UserInfoActivity.class);
                    startActivity(intent);
                    finish();
                } else if (object.getString("command").equals("Server is initialized")) {
                    ServerInitObj obj = new Gson().fromJson(s, ServerInitObj.class);
                    Intent intent = new Intent(MainActivity.this, WarnStepOneActivity.class);
                    SharePreferenceUtils.getInstance(getApplicationContext()).saveServerInitInfo(obj.getProperty());
                    startActivity(intent);
                    finish();
                }
        } catch(
        JSONException e)

        {
            e.printStackTrace();
        }
    }

    @Override
    public void socketConnectSuccess() {
        dialog.dismiss();
        Toast.makeText(MainActivity.this, "connect success", Toast.LENGTH_SHORT).show();
        ServerInfo info = new ServerInfo();
        info.setIp(ip.getText().toString());
        info.setPort(Integer.parseInt(port.getText().toString()));
        SharePreferenceUtils.getInstance(getApplicationContext()).saveServerInfo(info);
        //发送初始化数据
        JSONObject object = new JSONObject();
        try {
            object.put("command", "isInitialized");
            ClientManager.getInstance().sendData(object.toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
};

@Override
protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ip=findViewById(R.id.ip_address);
        port=findViewById(R.id.port);
        connect=findViewById(R.id.connect);
        connect.setOnClickListener(this);
        dialog=new ProgressDialog(this);
        dialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        SocketEventObserver.getInstance().addObserve(listener);
        ServerInfo info=SharePreferenceUtils.getInstance(this).getServerInfo();
        if(info!=null){
        ip.setText(info.getIp());
        port.setText(String.valueOf(info.getPort()));
        connect.performClick();
        }else{

//            port.setText("");
//            ip.setText("");
        //this is test data
        port.setText("8888");
        ip.setText("192.168.1.100");
        }
        }

@Override
protected void onDestroy(){
        super.onDestroy();
        SocketEventObserver.getInstance().removeObserve(listener);
        }

@Override
public void onClick(View v){
        if(TextUtils.isEmpty(ip.getText().toString())||TextUtils.isEmpty(port.getText().toString())){
        Toast.makeText(this,"Please fill the information!",Toast.LENGTH_SHORT).show();
        return;
        }
        dialog.show();
        Intent intent=new Intent(this,ClientService.class);
        intent.putExtra("host",ip.getText().toString());
        intent.putExtra("port",Integer.parseInt(port.getText().toString()));
        ClientService.getInstance().onStartCommand(intent);
        }
        }
