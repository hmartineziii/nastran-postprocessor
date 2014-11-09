Attribute VB_Name = "Module1"

Option Base 1
Sub PP_File_f06()
'This program will open an f06 file with and produ
'This is a clunkier, less capable version of what's in the python script
'
Dim I As Integer
Dim J As Integer
Dim LC_count As Integer

Dim TextToFind As String
Dim TextTemp(10) As String
Dim FileName(10) As String          'Input File name Table of GPFO data
Dim OP_FileName(10) As String       'Output File name Table of GPFO data


Dim rf06 As Range
Set rf06 = Worksheets("PP_f06_Run").Range("D11:F20")
J = 1

OP_FileName(J) = rf06.Cells(J, 2)
Open ThisWorkbook.Path & "\" & OP_FileName(J) For Output As #2

Do While rf06.Cells(J, 1) <> ""

    FileName(J) = rf06.Cells(J, 1)
    
    'OP_FileName(J) = rf06.Cells(J, 2)
    
    LC_count = CInt(rf06.Cells(J, 3))
    





'LC_count = 5

I = 0



Open ThisWorkbook.Path & "\" & FileName(J) For Input As #1

'Open ThisWorkbook.Path & "\" & OP_FileName(J) For Output As #2

    TextToFind = "G R I D   P O I N T   F O R C E   B A L A N C E"
    '````````````````Loop to find gpfo or eof
    Do Until EOF(1)
    
        Line Input #1, DATA
      
            'Buffer to keep LC data for first gpfo
            TextTemp(3) = TextTemp(2)
            TextTemp(2) = TextTemp(1)
            TextTemp(1) = DATA
        
        'Check to find if gpfo data is contained
        
        If InStr(1, DATA, TextToFind) Then
        
        'Print GPFO title
        Print #2, DATA
        Print #2, FileName(J)
        'skip 3 lines
        Line Input #1, DATA
        Line Input #1, DATA
        Line Input #1, DATA
        
            TextTemp(1) = DATA
        'line changed for prelim_ult to 6, 16***************************
            TextTemp(4) = Mid(TextTemp(3), 6, 16)
            TextTemp(5) = Mid(TextTemp(1), 4)
            TextTemp(6) = TextTemp(4) & TextTemp(5)
           
            
            'the main table record format
            Print #2, TextTemp(6)
            
            
            'get data put in tem strg
            Line Input #1, DATA
            ' ----First data Line ---------#############
            
            TextTemp(1) = DATA
            
            'For I = 1 To LC_count------------------------------------
                Do Until EOF(1)
                    Do Until Left(TextTemp(1), 1) = "1"
                    
                    'get data put in tem strg
                        I = 1
                        
                        
                        TextTemp(5) = Mid(TextTemp(1), 4)
                        
                        TextTemp(6) = TextTemp(4) & TextTemp(5)
                    
                    
                        Print #2, TextTemp(6)
                        
                        'get data put in tem strg
                        Line Input #1, DATA
                        TextTemp(1) = DATA
                        
                    
                     'Print #2, data
                     Loop
                'line changed for prelim_ult to 6, 16***************************
            
                Line Input #1, DATA
                Line Input #1, DATA
                TextTemp(3) = DATA
                TextTemp(4) = Mid(TextTemp(3), 6, 16)
                Line Input #1, DATA
                Line Input #1, DATA
                Line Input #1, DATA
                Line Input #1, DATA
                Line Input #1, DATA
                TextTemp(1) = DATA
                
                Loop
                
   
           ' Next
            
        End If
        
        
        

        'Print #2, TextTemp(6)
    
        
    
 
    Loop
    
    If I < 1 Then
    
    Range("C24").Select
    ActiveCell.FormulaR1C1 = "1 or more files has no G R I D   P O I N T   F O R C E   B A L A N C E  data found"
    End If


Close #1 'Close all files
J = J + 1
Loop

Close #2
End Sub
