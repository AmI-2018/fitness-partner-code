package client.clientfortask.activity;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.SwitchCompat;
import android.view.View;
import android.widget.CompoundButton;
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
import client.clientfortask.observer.SocketEventObserver;

public class WarnSportActivity extends BaseActivity implements SocketEventListener, View.OnClickListener, CompoundButton.OnCheckedChangeListener {

    public static final int PLAY_STATUS = 0;
    public static final int PAUSE_STATUS = 1;

    private TextView sportTime;
    private TextView music;
    private TextView operation;
    private TextView change;
    private TextView heart;
    private SwitchCompat light_switch;
    private TextView stop;
    private TextView settings;

    private int currentStatus;
    private int time;
    private Handler handler = new Handler();
    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            time = time + 1;
            updateWarmTime();
            handler.postDelayed(this, 1000);
        }
    };

    private void updateWarmTime() {
        int minute = time / 60;
        int seconds = time % 60;
        StringBuffer buffer = new StringBuffer();
        buffer.append(minute < 10 ? "0" + minute : minute).append(":").append(seconds < 10 ? "0" + seconds : seconds);
        sportTime.setText(buffer.toString());
    }

    private void updateOperationStatus() {
        if (currentStatus == PLAY_STATUS) operation.setText("PAUSE");
        else if (currentStatus == PAUSE_STATUS) operation.setText("PLAY");
    }

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_warn_sport);
        SocketEventObserver.getInstance().addObserve(this);
        sportTime = findViewById(R.id.wake_up_time);
        music = findViewById(R.id.music_name);
        operation = findViewById(R.id.operation);
        change = findViewById(R.id.random);
        heart = findViewById(R.id.heart);
        light_switch = findViewById(R.id.light_switch);
        stop = findViewById(R.id.stop);
        settings =findViewById(R.id.settings);

        operation.setOnClickListener(this);
        change.setOnClickListener(this);
        light_switch.setOnCheckedChangeListener(this);
        stop.setOnClickListener(this);
        settings.setOnClickListener(this);

        time = 0;
        currentStatus = 0;
        updateOperationStatus();
        handler.post(runnable);
        updateWarmTime();
        Map<String, String> map = new HashMap<>();
        map.put("command", "Start sport music");
        JSONObject object = new JSONObject(map);
        ClientManager.getInstance().sendData(object.toString());
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        SocketEventObserver.getInstance().removeObserve(this);
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
                music.setText(obj.getData());
            } else if (obj.getCommand().equals("Heartbeat rate")) {
                heart.setText("Heart Beat:" + obj.getData());
            }else if (obj.getCommand().equals("Quit client")){
                finish();
            }
            return;
        } catch (Exception e) {

        }
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
            currentStatus = 0;
            updateOperationStatus();
        }else if (v== stop){
            AlertDialog dialog = new AlertDialog.Builder(this).setMessage("Do you want to end your exerices").setPositiveButton("YES", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    Map<String,String> map = new HashMap<>();
                    map.put("command","Quit client");
                    JSONObject object = new JSONObject(map);
                    ClientManager.getInstance().sendData(object.toString());
                }
            }).setNegativeButton("NO", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {

                }
            }).create();
            dialog.show();
        }else if (v==settings){
            Intent intent= new Intent(this,SettingsActivity.class);
            startActivity(intent);
        }
    }

    @Override
    public void onBackPressed() {
        stop.performLongClick();
    }

    @Override
    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
        Map<String, String> map = new HashMap<>();
        map.put("command", isChecked?"Start light module": "Stop light module");
        JSONObject object = new JSONObject(map);
        ClientManager.getInstance().sendData(object.toString());
    }
}
