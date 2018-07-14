package client.clientfortask.activity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.google.gson.Gson;

import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import client.clientfortask.R;
import client.clientfortask.listener.SocketEventListener;
import client.clientfortask.manager.ClientManager;
import client.clientfortask.obj.HeartBeatObj;
import client.clientfortask.obj.Mode;
import client.clientfortask.obj.ServerInitSuccessObj;
import client.clientfortask.observer.SocketEventObserver;

public class HeartBeatActivity extends BaseActivity implements SocketEventListener, View.OnClickListener {
    private int num = 0;
    private List<Integer> data = new ArrayList<>();
    private TextView result;
    private Button start;
    private EditText heartbeat;
    private Button ok;
    private int heart_beat = -1;
    private ProgressDialog dialog;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.heart_beat_activity);
        heartbeat = findViewById(R.id.age);
        heartbeat.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                heart_beat = Integer.parseInt(s.toString());
            }
        });
        result = findViewById(R.id.result);
        start = findViewById(R.id.start);
        dialog = new ProgressDialog(this);
        dialog.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
        dialog.setMax(15);
        dialog.setProgress(num);
        ok = findViewById(R.id.ok);
        SocketEventObserver.getInstance().addObserve(this);
        ok.setOnClickListener(this);
        start.setOnClickListener(this);

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
            HeartBeatObj obj = new Gson().fromJson(s, HeartBeatObj.class);
            if (obj.getCommand().equals("Heartbeat rate")) {
                data.add(obj.getData());
            }
            num++;
            dialog.setProgress(num);
            average();
            if (num == 15) dialog.dismiss();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void average() {
        int total = 0;
        for (int index = 0; index < data.size(); index++) {
            total = total + data.get(index);
        }
        heart_beat = total / data.size();
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onEvent(ServerInitSuccessObj obj){
        finish();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        SocketEventObserver.getInstance().removeObserve(this);
    }

    @Override
    public void onClick(View v) {
        if (v == start) {
            Map<String, String> map = new HashMap<>();
            map.put("command", "Get rest heartbeat rate");
            JSONObject object = new JSONObject(map);
            data.clear();
            num =0;
            ClientManager.getInstance().sendData(object.toString());
            dialog.show();
        } else if (v == ok) {
            Mode.getInstance().setHeart(heart_beat);
            Intent intent = new Intent(this,UserInfoTimeActivity.class);
            startActivity(intent);
        }
    }
}
