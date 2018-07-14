package client.clientfortask.activity;

import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.TextView;

import com.google.gson.Gson;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

import client.clientfortask.R;
import client.clientfortask.listener.SimpleSocketEventListener;
import client.clientfortask.listener.SocketEventListener;
import client.clientfortask.manager.ClientManager;
import client.clientfortask.obj.ColorUpdateObj;
import client.clientfortask.obj.LightCommandObj;
import client.clientfortask.obj.MusicSocketObj;
import client.clientfortask.observer.SocketEventObserver;

public class ColorSettingsActivity extends BaseActivity implements View.OnClickListener {
    private int[] color1 = new int[]{255, 255, 255};
    private int[] color2 = new int[]{0, 191, 255};
    private int[] color3 = new int[]{153, 204, 51};
    private int[] color4 = new int[]{143, 188, 143};
    private int[] color5 = new int[]{255, 68, 0};
    private int[] color6 = new int[]{210, 105, 30};

    private TextView colortext1;
    private TextView colortext2;
    private TextView colortext3;
    private TextView colortext4;
    private TextView colortext5;
    private TextView colortext6;

    private int[] currentcolor1 = new int[]{255, 255, 255};
    private int[] currentcolor2 = new int[]{153, 204, 51};
    private int[] currentcolor3 = new int[]{255, 68, 0};

    private TextView usercolor1;
    private TextView usercolor2;
    private TextView usercolor3;
    private TextView apply;
    private SimpleSocketEventListener listener = new SimpleSocketEventListener(){
        @Override
        public void socketReceviedData(String s) {
            super.socketReceviedData(s);
            try {
                MusicSocketObj obj = new Gson().fromJson(s, MusicSocketObj.class);
                if (obj.getCommand().equals("Update color successfully")) {
                    AlertDialog dialog = new AlertDialog.Builder(ColorSettingsActivity.this).setMessage(obj.getCommand()).setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                        }
                    }).create();
                    dialog.show();
                }
            }catch (Exception e){

            }
        }
    };


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_color_settings);
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
        apply.setOnClickListener(this);
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
                System.arraycopy(obj.rgb,0,currentcolor1,0,obj.rgb.length);
                break;
            case 2:
                System.arraycopy(obj.rgb,0,currentcolor2,0,obj.rgb.length);
                break;
            case 3:
                System.arraycopy(obj.rgb,0,currentcolor3,0,obj.rgb.length);
                break;
            default:
                break;
        }
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
            case R.id.stop:
                LightCommandObj obj = new LightCommandObj();
                obj.setCommand("Update light color");
                LightCommandObj.Data data = new LightCommandObj.Data();
                for (int index = 0; index < 3; index++) {
                    data.getDefault_color().add(currentcolor1[index]);
                    data.getAnaerobic_color().add(currentcolor2[index]);
                    data.getMaximum_color().add(currentcolor3[index]);
                }
                obj.setData(data);
                ClientManager.getInstance().sendData(new Gson().toJson(obj));
                break;
            default:
                break;
        }
    }
}
