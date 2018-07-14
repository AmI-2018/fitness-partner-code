package client.clientfortask.activity;

import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.SeekBar;

import org.greenrobot.eventbus.EventBus;

import java.util.ArrayList;
import java.util.List;

import client.clientfortask.R;
import client.clientfortask.obj.ColorUpdateObj;

public class RGBColorActivity extends BaseActivity implements SeekBar.OnSeekBarChangeListener {

    private ImageView color;
    private SeekBar red;
    private SeekBar green;
    private SeekBar blue;
    private int index;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_photo_rgb_color);
        index = getIntent().getIntExtra("index", -1);
        color = (ImageView) findViewById(R.id.color_img);
        red = (SeekBar) findViewById(R.id.red);
        green = (SeekBar) findViewById(R.id.green);
        blue = (SeekBar) findViewById(R.id.blue);
        findViewById(R.id.ok).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ColorUpdateObj obj = new ColorUpdateObj();
                obj.index = index;
                int[] rgb = new int[3];
                rgb[0] = (red.getProgress());
                rgb[1] = (green.getProgress());
                rgb[2] = (blue.getProgress());
                obj.rgb = rgb;
                EventBus.getDefault().post(obj);
                finish();
            }
        });

        red.setOnSeekBarChangeListener(this);
        green.setOnSeekBarChangeListener(this);
        blue.setOnSeekBarChangeListener(this);

        setImageColor();
    }

    private void setImageColor() {
        int redColor = red.getProgress();
        int blueColor = blue.getProgress();
        int greenColor = green.getProgress();
        String s1 = String.format("%02x", redColor);
        String s2 = String.format("%02x", blueColor);
        String s3 = String.format("%02x", greenColor);
        Log.e("yinjinbiao", "s1 is " + s1 + " s2 is " + s2 + " s3 is " + s3);
        color.setImageDrawable(new ColorDrawable(Color.parseColor("#" + s1 + s2 + s3)));
    }

    @Override
    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
        switch (seekBar.getId()) {
            case R.id.red:
                setColorRed();
                break;
            case R.id.green:
                setColorGreen();
                break;
            case R.id.blue:
                setColorBlue();
                break;
        }
    }

    @Override
    public void onStartTrackingTouch(SeekBar seekBar) {

    }

    @Override
    public void onStopTrackingTouch(SeekBar seekBar) {
        switch (seekBar.getId()) {
            case R.id.red:
                setColorRed();
                break;
            case R.id.green:
                setColorGreen();
                break;
            case R.id.blue:
                setColorBlue();
                break;
        }
    }

    private void setColorRed() {
        setImageColor();
    }

    private void setColorGreen() {
        setImageColor();
    }

    private void setColorBlue() {
        setImageColor();
    }
}
