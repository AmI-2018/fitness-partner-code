package client.clientfortask.activity;

import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import com.google.gson.Gson;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import client.clientfortask.R;
import client.clientfortask.listener.SimpleSocketEventListener;
import client.clientfortask.manager.ClientManager;
import client.clientfortask.obj.ColorUpdateObj;
import client.clientfortask.obj.LightCommandObj;
import client.clientfortask.obj.Mode;
import client.clientfortask.obj.MusicSocketObj;
import client.clientfortask.obj.ServerInitCommandObj;
import client.clientfortask.obj.ServerInitObj;
import client.clientfortask.obj.ServerInitSuccessObj;
import client.clientfortask.obj.WakeUpTimeObj;
import client.clientfortask.observer.SocketEventObserver;
import client.clientfortask.utils.SharePreferenceUtils;

public class UserInfoTimeActivity extends BaseActivity implements View.OnClickListener {

    private int[] color1 = new int[]{255, 180, 20};
    private int[] color2 = new int[]{100, 180, 20};
    private int[] color3 = new int[]{2, 180, 20};
    private int[] color4 = new int[]{4, 4, 20};
    private int[] color5 = new int[]{255, 180, 0};
    private int[] color6 = new int[]{99, 180, 20};

    private TextView colortext1;
    private TextView colortext2;
    private TextView colortext3;
    private TextView colortext4;
    private TextView colortext5;
    private TextView colortext6;

    private int[] currentcolor1 = new int[]{255, 180, 20};
    private int[] currentcolor2 = new int[]{2, 180, 20};
    private int[] currentcolor3 = new int[]{255, 180, 0};
    private int currentTime = 30;
    private int wake_time = 15;
    private String user_name="";
    private String user_pwd = "";

    private EditText wake_up_time;
    private TextView time1;
    private TextView time2;
    private TextView time3;
    private TextView user_time;
    private TextView usercolor1;
    private TextView usercolor2;
    private TextView usercolor3;
    private TextView apply;
    private EditText name;
    private EditText password;


    private SimpleSocketEventListener listener = new SimpleSocketEventListener() {
        @Override
        public void socketReceviedData(String s) {
            super.socketReceviedData(s);
            try {
                JSONObject object = new JSONObject(s);
                if (object.getString("command").equals("Initialized successfully")){
                    Intent intent = new Intent(UserInfoTimeActivity.this,WarnStepOneActivity.class);
                    startActivity(intent);
                    EventBus.getDefault().post(new ServerInitSuccessObj());
                }
            } catch (Exception e) {

            }
        }
    };

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onEvent(ServerInitSuccessObj obj){
        finish();
    }


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.user_info_time_activity);
        wake_up_time = findViewById(R.id.wake_up_time);
        wake_up_time.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                wake_time = Integer.parseInt(s.toString());
            }
        });
        time1 = findViewById(R.id.time1);
        time2 = findViewById(R.id.time2);
        time3 = findViewById(R.id.time3);
        user_time = findViewById(R.id.user_time);
        colortext1 = findViewById(R.id.color1);
        colortext2 = findViewById(R.id.color2);
        colortext3 = findViewById(R.id.color3);
        colortext4 = findViewById(R.id.color4);
        colortext5 = findViewById(R.id.color5);
        colortext6 = findViewById(R.id.color6);
        apply = findViewById(R.id.stop);
        usercolor1 = findViewById(R.id.user_color1);
        usercolor2 = findViewById(R.id.user_color2);
        usercolor3 = findViewById(R.id.user_color3);
        name = findViewById(R.id.name);
        password = findViewById(R.id.secret);

        name.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                user_name = s.toString();
            }
        });
        password.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {

            }

            @Override
            public void afterTextChanged(Editable s) {
                user_pwd = s.toString();
            }
        });

        colortext1.setBackgroundDrawable(new ColorDrawable(Color.rgb(color1[0], color1[1], color1[2])));
        colortext2.setBackgroundDrawable(new ColorDrawable(Color.rgb(color2[0], color2[1], color2[2])));
        colortext3.setBackgroundDrawable(new ColorDrawable(Color.rgb(color3[0], color3[1], color3[2])));
        colortext4.setBackgroundDrawable(new ColorDrawable(Color.rgb(color4[0], color4[1], color4[2])));
        colortext5.setBackgroundDrawable(new ColorDrawable(Color.rgb(color5[0], color5[1], color5[2])));
        colortext6.setBackgroundDrawable(new ColorDrawable(Color.rgb(color6[0], color6[1], color6[2])));

        colortext1.setOnClickListener(this);
        colortext2.setOnClickListener(this);
        colortext3.setOnClickListener(this);
        colortext4.setOnClickListener(this);
        colortext5.setOnClickListener(this);
        colortext6.setOnClickListener(this);
        usercolor1.setOnClickListener(this);
        usercolor2.setOnClickListener(this);
        usercolor3.setOnClickListener(this);
        user_time.setOnClickListener(this);
        apply.setOnClickListener(this);
        time1.setOnClickListener(this);
        time2.setOnClickListener(this);
        time3.setOnClickListener(this);
        SocketEventObserver.getInstance().addObserve(listener);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        SocketEventObserver.getInstance().removeObserve(listener);
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onEvent(ColorUpdateObj obj) {
        switch (obj.index) {
            case 1:
                System.arraycopy(obj.rgb, 0, currentcolor1, 0, obj.rgb.length);
                break;
            case 2:
                System.arraycopy(obj.rgb, 0, currentcolor2, 0, obj.rgb.length);
                break;
            case 3:
                System.arraycopy(obj.rgb, 0, currentcolor3, 0, obj.rgb.length);
                break;
            default:
                break;
        }
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onEvent(WakeUpTimeObj obj) {
            currentTime = obj.time;
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.color1:
                System.arraycopy(color1, 0, currentcolor1, 0, color1.length);
                break;
            case R.id.color2:
                System.arraycopy(color2, 0, currentcolor1, 0, color2.length);
                break;
            case R.id.color3:
                System.arraycopy(color3, 0, currentcolor2, 0, color3.length);
                break;
            case R.id.color4:
                System.arraycopy(color4, 0, currentcolor2, 0, color4.length);
                break;
            case R.id.color5:
                System.arraycopy(color5, 0, currentcolor3, 0, color5.length);
                break;
            case R.id.color6:
                System.arraycopy(color6, 0, currentcolor3, 0, color6.length);
                break;
            case R.id.user_color1:
                Intent intent = new Intent(this, RGBColorActivity.class);
                intent.putExtra("index", 1);
                startActivity(intent);
                break;
            case R.id.user_color2:
                intent = new Intent(this, RGBColorActivity.class);
                intent.putExtra("index", 2);
                startActivity(intent);
                break;
            case R.id.user_color3:
                intent = new Intent(this, RGBColorActivity.class);
                intent.putExtra("index", 3);
                startActivity(intent);
                break;
            case R.id.time1:
                currentTime = 30;
                break;
            case R.id.time2:
                currentTime = 45;
                break;
            case R.id.time3:
                currentTime = 60;
                break;
            case R.id.user_time:
                intent =new Intent(this,ServerRestTimeActivity.class);
                startActivity(intent);
                break;
            case R.id.stop:
                initServer();
                break;
            default:
                break;
        }
    }

    private void initServer() {
        ServerInitCommandObj obj = new ServerInitCommandObj();
        obj.setCommand("Initialize");
        ServerInitCommandObj.DataBean dataBean = new ServerInitCommandObj.DataBean();
        dataBean.setAge(Mode.getInstance().getAge());
        dataBean.setRest_heartbeat_rate(Mode.getInstance().getHeart());
        List<Integer> list1 = new ArrayList<>();
        List<Integer> list2 = new ArrayList<>();
        List<Integer> list3 = new ArrayList<>();
        for (int index =0;index<3;index++){
            list1.add(color1[index]);
            list2.add(color2[index]);
            list3.add(color3[index]);
        }
        dataBean.setDefault_color(list1);
        dataBean.setAnaerobic_color(list2);
        dataBean.setMaximum_color(list3);
        dataBean.setFitbit_user_id(user_name);
        dataBean.setFitbit_user_secret(user_pwd);
        dataBean.setWarm_up_time(wake_time);
        dataBean.setRest_time(currentTime);
        obj.setData(dataBean);
        ServerInitObj.PropertyInfo propertyInfo = new ServerInitObj.PropertyInfo();
        propertyInfo.setDefault_color(list1);
        propertyInfo.setAnaerobic_color(list2);
        propertyInfo.setMaximum_color(list3);
        propertyInfo.setWarm_up_time(wake_time);
        SharePreferenceUtils.getInstance(getApplicationContext()).saveServerInitInfo(propertyInfo);
        ClientManager.getInstance().sendData(new Gson().toJson(obj));
    }
}
