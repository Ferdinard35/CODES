<?php
$number1 = 50;
$number2 = 50;
$array = [1, 2, 3, 4, 5];
foreach ($array as $value) {
    echo $value . " ";
}
echo "\n";
if ($number1 > $number2) {
    echo "Number 1 is greater than Number 2";
} elseif ($number2 > $number1) {
    echo "Number 2 is greater than Number 1";
} else {
    echo "Number 1 and Number 2 are equal";
}
echo "\n";
$option = 1;
switch ($option) {
    case 1:
        echo "Option 1 selected";
        break;
    case 2:
        echo "Option 2 selected";
        break;
    case 3:
        echo "Option 3 selected";
        break;
    default:
        echo "Invalid option selected";
}
echo "\n";
function add($number1, $number2)
{
    return $number1 + $number2;
}
echo add($number1, $number2);
