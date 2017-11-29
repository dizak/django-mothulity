from django import forms

input_class = "w3-input"


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True,
                                                                        "class": input_class,
                                                                        "autocomplete": "off"}))


class OptionsForm(forms.Form):
    job_name = forms.CharField(label="Name of your job. It will be displayed\
                               in the results.",
                               max_length=20,
                               error_messages={"required": ""},
                               widget=forms.
                               TextInput(attrs={"value": "",
                                                "class": input_class}))
    notify_email = forms.EmailField(label="e-mail address on which you will be\
                                    notified",
                                    max_length=40,
                                    widget=forms.
                                    EmailInput(attrs={"value": "",
                                                      "class": input_class}))
    max_ambig = forms.IntegerField(label="Maximum number of ambiguous bases\
                                   allowed.",
                                   widget=forms.
                                   TextInput(attrs={"value": 0,
                                                    "class": input_class}))
    max_homop = forms.IntegerField(label="Maximum number of homopolymers allowed.",
                                   widget=forms.
                                   TextInput(attrs={"value": 8,
                                                    "class": input_class}))
    min_length = forms.IntegerField(label="Minimum length of read allowed.",
                                    widget=forms.
                                    TextInput(attrs={"value": 400,
                                                     "class": input_class}))
    max_length = forms.IntegerField(label="Maximum length of read allowed.",
                                    widget=forms.
                                    TextInput(attrs={"value": 500,
                                                     "class": input_class}))
    min_overlap = forms.IntegerField(label="Minimum number of bases overlap in\
                                     contig",
                                     widget=forms.
                                     TextInput(attrs={"value": 25,
                                                      "class": input_class}))
    screen_criteria = forms.IntegerField(label="Trim start and end of read to fit\
                                         this percentage of all reads",
                                         widget=forms.
                                         TextInput(attrs={"value": 95,
                                                          "class": input_class}))
    chop_length = forms.IntegerField(label=" Cut all the reads to this length.\
                                     Keeps front of the sequences",
                                     widget=forms.
                                     TextInput(attrs={"value": 250,
                                                      "class": input_class}))
    precluster_diffs = forms.IntegerField(label="Number of differences between\
                                          reads treated as insignificant.",
                                          widget=forms.
                                          TextInput(attrs={"value": 2,
                                                           "class": input_class}))
    classify_seqs_cutoff = forms.IntegerField(label="Bootstrap value for taxonomic\
                                              assignment.",
                                              widget=forms.
                                              TextInput(attrs={"value": 80,
                                                               "class": input_class}))
    amplicon_type = forms.ChoiceField(label="Amplicon type.",
                                      choices=[("16S", "16S"),
                                               ("ITS", "ITS")],
                                      widget=forms.
                                      RadioSelect())
