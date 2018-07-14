package client.clientfortask.activity;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.widget.Toast;

import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import client.clientfortask.listener.SimpleSocketEventListener;
import client.clientfortask.manager.ClientManager;
import client.clientfortask.obj.ServerInfo;
import client.clientfortask.obj.ServerInitObj;
import client.clientfortask.observer.SocketEventObserver;
import client.clientfortask.service.ClientService;
import client.clientfortask.utils.SharePreferenceUtils;

public class WelcomeActivity extends BaseActivity {

    private ProgressDialog dialog;
    private SimpleSocketEventListener listener = new SimpleSocketEventListener() {
        @Override
        public void socketConnectFailed() {
            dialog.dismiss();
            Toast.makeText(WelcomeActivity.this, "connect failed ", Toast.LENGTH_SHORT).show();
            AlertDialog alertDialog = new AlertDialog.Builder(WelcomeActivity.this).setMessage("Connection failed!").setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    Intent intent = new Intent(WelcomeActivity.this, MainActivity.class);
                    startActivity(intent);
                    finish();
                }
            }).create();
            alertDialog.show();
        }

        @Override
        public void socketReceviedData(String s) {
            super.socketReceviedData(s);
            try {
                JSONObject object = new JSONObject(s);
                if (object.getString("command").equals("Server isn't initialized")){
                    Intent intent = new Intent(WelcomeActivity.this,UserInfoActivity.class);
                    startActivity(intent);
                    finish();
                } else if (object.getString("command").equals("Server is initialized")){
                    ServerInitObj obj = new Gson().fromJson(s,ServerInitObj.class);
                    Intent intent = new Intent(WelcomeActivity.this,WarnStepOneActivity.class);
                    SharePreferenceUtils.getInstance(getApplicationContext()).saveServerInitInfo(obj.getProperty());
                    startActivity(intent);
                    finish();
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }

        }

        @Override
        public void socketConnectSuccess() {
            dialog.dismiss();
            Toast.makeText(WelcomeActivity.this, "connect success", Toast.LENGTH_SHORT).show();
            //发送初始化数据
            JSONObject object= new JSONObject();
            try {
                object.put("command","isInitialized");
                ClientManager.getInstance().sendData(object.toString());
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        SocketEventObserver.getInstance().removeObserve(listener);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ClientService.getInstance().onDestroy();
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                dialog = new ProgressDialog(WelcomeActivity.this);
                dialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
                SocketEventObserver.getInstance().addObserve(listener);
                ServerInfo serverInfo = SharePreferenceUtils.getInstance(getApplicationContext()).getServerInfo();
                if (serverInfo == null) {
                    Intent intent = new Intent(WelcomeActivity.this,MainActivity.class);
                    startActivity(intent);
                    finish();
                }else {
                    dialog.show();
                    Intent intent = new Intent(WelcomeActivity.this, ClientService.class);
                    intent.putExtra("host", serverInfo.getIp());
                    intent.putExtra("port", serverInfo.getPort());
                    ClientService.getInstance().onStartCommand(intent);
                }
            }
        },2000);


    }

}
