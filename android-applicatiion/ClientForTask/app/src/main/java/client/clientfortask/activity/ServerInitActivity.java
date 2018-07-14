package client.clientfortask.activity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.TextView;

import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

import client.clientfortask.R;
import client.clientfortask.listener.SocketEventListener;
import client.clientfortask.manager.ClientManager;
import client.clientfortask.obj.MusicSocketObj;
import client.clientfortask.obj.ServerInitObj;
import client.clientfortask.observer.SocketEventObserver;
import client.clientfortask.utils.SharePreferenceUtils;

public class ServerInitActivity extends BaseActivity implements View.OnClickListener, SocketEventListener {

    public static final int PLAY_STATUS = 0;
    public static final int PAUSE_STATUS = 1;

    public static int currentStatus;
    private TextView settings;
    private TextView wake_up_time;
    private TextView music_name;
    private TextView operation;
    private TextView change;
    private TextView start;
    private Handler handler = new Handler();
    private int time;
    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            time = time - 1;
            if (time < 0) {
                Map<String, String> command = new HashMap<>();
                command.put("command", "Start heartbeat detection");
                JSONObject object = new JSONObject(command);
                ClientManager.getInstance().sendData(object.toString());
                command.clear();
                command.put("command", "Start light module");
                object = new JSONObject(command);
                ClientManager.getInstance().sendData(object.toString());
                return;
            }
            updateWarmTime();
            handler.postDelayed(this, 1000);
        }
    };

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.server_init_activity);

        settings = findViewById(R.id.settings);
        wake_up_time = findViewById(R.id.wake_up_time);
        music_name = findViewById(R.id.music_name);
        operation = findViewById(R.id.operation);
        change = findViewById(R.id.random);
        start = findViewById(R.id.start);
        currentStatus = 0;
        ServerInitObj.PropertyInfo serverInitInfo = SharePreferenceUtils.getInstance(getApplicationContext()).getServerInitInfo();
        if (serverInitInfo == null){
            finish();
        }
        time = serverInitInfo.getWarm_up_time() * 60;
        updateWarmTime();
        handler.postDelayed(runnable, 1000);
        settings.setOnClickListener(this);
        operation.setOnClickListener(this);
        change.setOnClickListener(this);
        start.setOnClickListener(this);
        settings.setOnClickListener(this);
        updateOperationStatus();
        SocketEventObserver.getInstance().addObserve(this);
        Map<String, String> map = new HashMap<>();
        map.put("command", "Start warm up music");
        JSONObject object = new JSONObject(map);
        ClientManager.getInstance().sendData(object.toString());

    }

    private void updateWarmTime() {
        int minute = time / 60;
        int seconds = time % 60;
        StringBuffer buffer = new StringBuffer();
        buffer.append(minute < 10 ? "0" + minute : minute).append(":").append(seconds < 10 ? "0" + seconds : seconds);
        wake_up_time.setText(buffer.toString());
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        handler.removeCallbacks(runnable);
        SocketEventObserver.getInstance().removeObserve(this);
    }

    private void updateOperationStatus() {
        if (currentStatus == PLAY_STATUS) operation.setText("PAUSE");
        else if (currentStatus == PAUSE_STATUS) operation.setText("PLAY");
    }

    @Override
    public void onClick(View v) {
        if (v == operation) {
            if (currentStatus == PLAY_STATUS) {
                currentStatus = PAUSE_STATUS;
                updateOperationStatus();
                JSONObject object = new JSONObject();
                try {
                    object.put("command", "Pause");
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                ClientManager.getInstance().sendData(object.toString());
            } else {
                currentStatus = PLAY_STATUS;
                updateOperationStatus();
                JSONObject object = new JSONObject();
                try {
                    object.put("command", "unPause");
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                ClientManager.getInstance().sendData(object.toString());
            }
        } else if (v == change) {
            JSONObject object = new JSONObject();
            try {
                object.put("command", "Change music");
            } catch (JSONException e) {
                e.printStackTrace();
            }
            ClientManager.getInstance().sendData(object.toString());
            currentStatus =0;
            updateOperationStatus();
        } else if (v == start) {
            Map<String, String> map = new HashMap<>();
            map.put("command", "Stop music module");
            JSONObject object = new JSONObject(map);
            ClientManager.getInstance().sendData(object.toString());
        }else if (v== settings){
            Intent intent = new Intent(this,SettingsActivity.class);
            startActivity(intent);
        }
    }

    @Override
    public void socketConnectSuccess() {

    }

    @Override
    public void socketConnectFailed() {

    }

    @Override
    public void socketReceviedData(String s) {
        try {
            MusicSocketObj obj = new Gson().fromJson(s, MusicSocketObj.class);
            if (obj.getCommand().equals("Music name")) {
                music_name.setText(obj.getData());
            } else if (obj.getCommand().equals("Music stopped")) {
                Intent intent = new Intent(this, WarnSportActivity.class);
                startActivity(intent);
                finish();
            }
            return;
        } catch (Exception e) {

        }
    }
}
