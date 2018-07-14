package client.clientfortask.activity;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

import client.clientfortask.R;
import client.clientfortask.obj.ServerInitSuccessObj;
import client.clientfortask.obj.WakeUpTimeObj;

public class ServerRestTimeActivity extends BaseActivity implements View.OnClickListener {

    private EditText time;
    private View ok;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_wake_up);
        time = findViewById(R.id.age);
        ok = findViewById(R.id.ok);
        ok.setOnClickListener(this);
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onEvent(ServerInitSuccessObj obj){
        finish();
    }

    @Override
    public void onClick(View v) {
        if (TextUtils.isEmpty(time.getText().toString())){
            Toast.makeText(this, "请输入时间", Toast.LENGTH_SHORT).show();
            return;
        }
        WakeUpTimeObj obj = new WakeUpTimeObj();
        obj.time = Integer.parseInt(time.getText().toString());
        obj.type = 1;
        EventBus.getDefault().post(obj);
        finish();
    }
}
