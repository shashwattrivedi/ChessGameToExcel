Sub FormatCells()
    Dim wks As Worksheet
    For Each wks In ActiveWorkbook.Worksheets
     
        wks.Activate
        ActiveWindow.Zoom = 25
        
         With wks
        .Cells.RowHeight = 10
        .Cells.ColumnWidth = 1
        
        End With
     
    Next wks
    MsgBox "Done"
End Sub

' colouring all sheets
' -----------------------------------------------------------------------------------------------------------------

Option Explicit

' ----------------------------------------------------------------
' Procedure Name: updateColour
' Procedure Kind: Sub
' Procedure Access: Public
' Author: Shashwat Trivedi
' Date: 04/09/2021
' ----------------------------------------------------------------
Sub updateColourForAllSheets()

    Dim cell As Range
    Dim rng As Range
    Dim MyValue As Variant
    Dim wks As Worksheet
    For Each wks In ActiveWorkbook.Worksheets

        Set rng = wks.Range("A1:FD160")
    
        For Each cell In rng.Cells
            Debug.Print cell.Address, cell.Value
            MyValue = f_setRGBCellBackground(cell)
        
        Next cell
        
    Next wks

End Sub

' ----------------------------------------------------------------
' Procedure Name: f_setRGBCellBackground
' Purpose: set the cell background corresponding to value
' Procedure Kind: Function
' Procedure Access: Public
' Parameter cell (Range): a cell as range
' Return Type: Variant
' Author: Shashwat Trivedi
' Date: 4/09/2021
' ----------------------------------------------------------------
Function f_setRGBCellBackground(cell As Range)

    Dim backGroundColor As Long
    Dim red As Long
    Dim green As Long
    Dim blue As Long
    Const zero As Long = 0
    backGroundColor = cell.Value
    If backGroundColor = 0 Then
        backGroundColor = zero
    End If
    
    cell.Interior.Color = backGroundColor
    
End Function


' -----------------------------------------------------------------------------------------------------------------


' Getting colour values
' -----------------------------------------------------------------------------------------------------------------


Option Explicit

' ----------------------------------------------------------------
' Procedure Name: updateCellValue
' Procedure Kind: Sub
' Procedure Access: Public
' Author: Shashwat Trivedi
' Date: 04/09/2021
' ----------------------------------------------------------------
Sub updateCellValue()

    Dim cell As Range
    Dim rng As Range
    Dim MyValue As Variant
    Set rng = Sheet1.Range(Cells(1, 1), Cells(50, 50))

    For Each cell In rng.Cells
        Debug.Print cell.Address, cell.Value
        MyValue = f_setRGBCellBackgroundColorValue(cell)
    
    Next cell

End Sub

' ----------------------------------------------------------------
' Procedure Name: f_setRGBCellBackgroundColorValue
' Purpose: set the RGB value on the cell
' Procedure Kind: Function
' Procedure Access: Public
' Parameter cell (Range): a cell as range
' Return Type: Variant
' Author: Shashwat Trivedi
' Date: 4/09/2021
' ----------------------------------------------------------------
Function f_setRGBCellBackgroundColorValue(cell As Range)

    Dim backGroundColor As Long
    Dim red As Long
    Dim green As Long
    Dim blue As Long
    Const zero As Long = 0
    backGroundColor = cell.Interior.Color
    If backGroundColor = 0 Then
        backGroundColor = zero
    End If
    
    cell.Value = backGroundColor
    
End Function






' -----------------------------------------------------------------------------------------------------------------

