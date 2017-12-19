from django import forms

input_class = "w3-input"


class FileFieldForm(forms.Form):
    """
    Form for multiple files upload.
    """
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True,
                                                                        "class": input_class,
                                                                        "autocomplete": "off"}))


class OptionsForm(forms.Form):
    """
    Form for specifying analysis options and parameters.
    """
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
    max_homop = forms.IntegerField(label="Maximum number of homopolymers\
                                   allowed.",
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
    screen_criteria = forms.IntegerField(label="Trim start and end of the read\
                                         will be selected to fit these values\
                                         of that percentage of all reads",
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
                                              assignment. Minimum value of\
                                              read similarity to database when\
                                              performing taxonomic assignment.",
                                              widget=forms.
                                              TextInput(attrs={"value": 80,
                                                               "class": input_class}))
    amplicon_type = forms.ChoiceField(label="Amplicon type.",
                                      choices=[("16S", "16S"),
                                               ("ITS", "ITS")],
                                      widget=forms.
                                      RadioSelect())

    def clean(self):
        """
        Validates if min_length is not greater than max_length. Passes proper
        information to OptionsForm._errors and deletes value from
        OptionsForm.cleaned_data.
        """
        if self.cleaned_data["min_length"] >= self.cleaned_data["max_length"]:
            self._errors["min_length"] = ["min_length > max_length"]
            self._errors["max_length"] = ["max_length < min_length"]
            del self.cleaned_data["min_length"]

    def clean_max_homop(self):
        """
        Validates if clean_max_homop is non-zero nor ridiculously large
        """
        if self.cleaned_data["max_homop"] > 20:
            raise forms.ValidationError("Must be below 20")
            self._errors["max_homop"] = ["Must be below 20"]
        return self.cleaned_data["max_homop"]

    def clean_min_overlap(self):
        """
        Validates if clean_min_overlap is non-zero nor ridiculously large
        """
        if self.cleaned_data["min_overlap"] == 0:
            raise forms.ValidationError("Must be non-zero value")
            self._errors["min_overlap"] = ["Must be non-zero value"]
        return self.cleaned_data["min_overlap"]

    def clean_screen_criteria(self):
        """
        Validates if clean_screen_criteria is non-zero nor ridiculously large
        """
        if self.cleaned_data["screen_criteria"] == 0:
            raise forms.ValidationError("Must be non-zero value")
            self._errors["screen_criteria"] = ["Must be non-zero value"]
        return self.cleaned_data["screen_criteria"]

    def clean_chop_length(self):
        """
        Validates if clean_chop_length is non-zero nor ridiculously large
        """
        if self.cleaned_data["chop_length"] == 0:
            raise forms.ValidationError("Must be non-zero value")
            self._errors["chop_length"] = ["Must be non-zero value"]
        return self.cleaned_data["chop_length"]

    def clean_precluster_diffs(self):
        """
        Validates if clean_precluster_diffs is non-zero nor ridiculously large
        """
        if self.cleaned_data["precluster_diffs"] == 0:
            raise forms.ValidationError("Must be non-zero value")
            self._errors["precluster_diffs"] = ["Must be non-zero value"]
        return self.cleaned_data["precluster_diffs"]

    def clean_classify_seqs_cutoff(self):
        """
        Validates if clean_classify_seqs_cutoff is non-zero nor ridiculously large
        """
        if self.cleaned_data["classify_seqs_cutoff"] == 0:
            raise forms.ValidationError("Must be non-zero value")
            self._errors["classify_seqs_cutoff"] = ["Must be non-zero value"]
        return self.cleaned_data["classify_seqs_cutoff"]

    def clean_job_name(self):
        self.cleaned_data["job_name"] = self.cleaned_data["job_name"].replace("-", "_")
        return self.cleaned_data["job_name"]
