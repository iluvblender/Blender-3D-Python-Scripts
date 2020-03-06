import bpy

import serial

class MicrobitSerialPortTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_microbit_operator"
    bl_label = "BBC Microbit Modal Timer Operator"

    _timer = None
    _serial = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # data = self._serial.read_until(serial.CR+serial.LF)
            data = self._serial.readline().decode()
            if data.strip():
                print(data)

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        try:
            self._serial = serial.Serial('COM5', 
                                         115200, 
                                         timeout=0, 
                                         bytesize=8, 
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         )
        except serial.serialutil.SerialException:
            print("Could not open serial port COM5")
        else:
            wm.modal_handler_add(self)
            print("Serial port COM5 connection is setup")
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        del(self._serial)
        self._serial = None
        print("Serial port COM5 connection is closed")


def register():
    bpy.utils.register_class(MicrobitSerialPortTimerOperator)


def unregister():
    bpy.utils.unregister_class(MicrobitSerialPortTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_microbit_operator()
