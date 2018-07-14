package client.clientfortask.activity;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.greenrobot.eventbus.Subscribe;
import org.greenrobot.eventbus.ThreadMode;

import client.clientfortask.R;
import client.clientfortask.obj.Mode;
import client.clientfortask.obj.ServerInitSuccessObj;

public class UserInfoActivity extends BaseActivity implements View.OnClickListener {

    private EditText age;
    private Button ok;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.user_info_activity);
        age = findViewById(R.id.age);
        ok = findViewById(R.id.ok);

        ok.setOnClickListener(this);
    }

    @Subscribe(threadMode = ThreadMode.MAIN)
    public void onEvent(ServerInitSuccessObj obj){
        finish();
    }

    @Override
    public void onClick(View v) {
        if (TextUtils.isEmpty(age.getText().toString())) {
            Toast.makeText(getApplicationContext(), "Please enter your age!", Toast.LENGTH_SHORT).show();
            return;
        }
        Mode.getInstance().setAge(Integer.parseInt(age.getText().toString()));
        Intent intent = new Intent(this,HeartBeatActivity.class);
        startActivity(intent);
    }
}
