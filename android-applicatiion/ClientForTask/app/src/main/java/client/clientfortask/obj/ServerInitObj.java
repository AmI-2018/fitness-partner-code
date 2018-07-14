package client.clientfortask.obj;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;
import java.util.List;

public class ServerInitObj implements Serializable{

    /**
     * command : Server is initialized
     * data : {"warm_up_time":15,"default_color":[255,255,255],"anaerobic_color":[153,204,51],"maximum_color":[255,68,0]}
     */

    private String command;
    @SerializedName("data")
    private PropertyInfo property;

    public String getCommand() {
        return command;
    }

    public void setCommand(String command) {
        this.command = command;
    }

    public PropertyInfo getProperty() {
        return property;
    }

    public void setProperty(PropertyInfo property) {
        this.property = property;
    }

    public static class PropertyInfo implements Serializable{
        /**
         * warm_up_time : 15
         * default_color : [255,255,255]
         * anaerobic_color : [153,204,51]
         * maximum_color : [255,68,0]
         */

        private int warm_up_time;
        private List<Integer> default_color;
        private List<Integer> anaerobic_color;
        private List<Integer> maximum_color;

        public int getWarm_up_time() {
            return warm_up_time;
        }

        public void setWarm_up_time(int warm_up_time) {
            this.warm_up_time = warm_up_time;
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
