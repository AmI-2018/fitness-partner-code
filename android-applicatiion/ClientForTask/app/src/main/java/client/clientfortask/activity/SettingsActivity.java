package client.clientfortask.activity;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Process;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.google.gson.Gson;

import org.greenrobot.eventbus.EventBus;
import org.json.JSONObject;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import client.clientfortask.R;
import client.clientfortask.listener.SimpleSocketEventListener;
import client.clientfortask.listener.SocketEventListener;
import client.clientfortask.manager.ClientManager;
import client.clientfortask.obj.ActivityFinishObj;
import client.clientfortask.obj.MusicSocketObj;
import client.clientfortask.obj.ServerInitObj;
import client.clientfortask.observer.SocketEventObserver;
import client.clientfortask.utils.SharePreferenceUtils;

public class SettingsActivity extends BaseActivity implements AdapterView.OnItemClickListener {

    private ListView listView;
    private int onclick;
    private ArrayAdapter<String> adapter;
    private String[] command = new String[]{"Update MDB successfully","Reset successfully"};
    private String[] data = new String[]{"Update music database", "Update light corlor", "Reset All settings", "Reset server settings", "About us"};
    private SimpleSocketEventListener listener = new SimpleSocketEventListener() {
        @Override
        public void socketReceviedData(String s) {
            try {
                handData(s);
            }catch (Exception e){

            }
        }
    };

    private void handData(String s) {
        try {
            MusicSocketObj obj = new Gson().fromJson(s, MusicSocketObj.class);
            if (obj.getCommand().equals("Quit client")){
                SocketEventObserver.getInstance().clear();
                EventBus.getDefault().post(new ActivityFinishObj());
                return;
            }
            if (!Arrays.asList(command).contains(obj.getCommand())) return;
            final String temp = obj.getCommand();
            if (obj.getCommand().equals(command[1])){
                if (onclick == 2){
                    obj.setCommand("Reset all settings successfully!");
                }else if (onclick == 3){
                    obj.setCommand("Reset server settings successfully!");
                }
            }
            AlertDialog dialog = new AlertDialog.Builder(this).setMessage(obj.getCommand()).setPositiveButton("OK", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                    if (temp.equals(command[1])){
                        Map<String,String> map = new HashMap<>();
                        map.put("command","Quit client");
                        JSONObject object = new JSONObject(map);
                        ClientManager.getInstance().sendData(object.toString());
                    }
                }
            }).create();
            dialog.setCanceledOnTouchOutside(false);
            dialog.setCancelable(false);
            dialog.show();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        listView = findViewById(R.id.list);
        listView.setOnItemClickListener(this);
        adapter = new ArrayAdapter<String>(this, R.layout.adapter_settings, data);
        listView.setAdapter(adapter);
        SocketEventObserver.getInstance().addObserve(listener);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        SocketEventObserver.getInstance().removeObserve(listener);
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        onclick = position;
        switch (position) {
            case 0:
                Map<String, String> map = new HashMap<>();
                map.put("command", "Update music database");
                JSONObject object = new JSONObject(map);
                ClientManager.getInstance().sendData(object.toString());
                break;
            case 1:
                Intent intent = new Intent(this,ColorSettingsActivity.class);
                startActivity(intent);
                break;
            case 2:
                map = new HashMap<>();
                map.put("command", "Reset server");
                object = new JSONObject(map);
                SharePreferenceUtils.getInstance(this).clear();
                ClientManager.getInstance().sendData(object.toString());
                break;
            case 3:
                map = new HashMap<>();
                map.put("command", "Reset server");
                object = new JSONObject(map);
                ClientManager.getInstance().sendData(object.toString());
                break;
            case 4:
                break;
            default:
                break;
        }
    }
}
