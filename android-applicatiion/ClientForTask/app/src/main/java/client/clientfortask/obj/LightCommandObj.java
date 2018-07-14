package client.clientfortask.obj;

import java.util.ArrayList;
import java.util.List;

public class LightCommandObj {

    /**
     * command : Update light color
     * data : {"default_color":[255,255,255],"anaerobic_color":[153,204,51],"maximum_color":[255,68,0]}
     */

    private String command;
    private Data data;

    public String getCommand() {
        return command;
    }

    public void setCommand(String command) {
        this.command = command;
    }

    public Data getData() {
        return data;
    }

    public void setData(Data data) {
        this.data = data;
    }

    public static class Data {
        private List<Integer> default_color;
        private List<Integer> anaerobic_color;
        private List<Integer> maximum_color;

        public Data (){
            default_color = new ArrayList<>(3);
            anaerobic_color = new ArrayList<>(3);
            maximum_color = new ArrayList<>(3);
        }

        public List<Integer> getDefault_color() {
            return default_color;
        }

        public void setDefault_color(List<Integer> default_color) {
            this.default_color = default_color;
        }

        public List<Integer> getAnaerobic_color() {
            return anaerobic_color;
        }

        public void setAnaerobic_color(List<Integer> anaerobic_color) {
            this.anaerobic_color = anaerobic_color;
        }

        public List<Integer> getMaximum_color() {
            return maximum_color;
        }

        public void setMaximum_color(List<Integer> maximum_color) {
            this.maximum_color = maximum_color;
        }

    }
}
