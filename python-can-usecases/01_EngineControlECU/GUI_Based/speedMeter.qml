import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Extras 1.4
import QtQuick.Controls 1.5

Window {
    id: window
    visible: true
    width: 350
    height: 480
    color: "#353333"
    title: qsTr("DashBoard")

    CircularGauge {
        id: circularGauge
        x: 37
        y: 61
        value: smManager.speedVal
        maximumValue: 150
    }

    ToggleButton {
        objectName: "brakBtn"
        id: toggleButton
        x: 62
        y: 406
        width: 65
        height: 55
        text: qsTr("Brake")
        checked: false
    }

    StatusIndicator {
        id: statusIndicator
        x: 227
        y: 407
        active: smManager.engStat
    }

    Slider {
        objectName: "AcclSlider"
        id: sliderHorizontal
        x: 37
        y: 356
        width: 272
        height: 22
        clip: false
        maximumValue: 150
        updateValueWhileDragging: true
        stepSize: 1
        activeFocusOnPress: true
        orientation: Qt.Horizontal
        tickmarksEnabled: false
        value: 0
    }

    Label {
        id: label
        x: 220
        y: 447
        color: "#d5d3d3"
        text: qsTr("Engine")
    }

    Label {
        id: label1
        x: 109
        y: 376
        color: "#d5d3d3"
        text: qsTr("Acceleration Pedel")
    }

    Label {
        id: label2
        x: 127
        y: 316
        color: "#d5d3d3"
        text: qsTr("Vehicle Speed")
    }
}
