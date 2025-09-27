# ... (all imports and code unchanged above) ...

class App:
    # ... (other methods unchanged) ...

    def _build_tab_items(self, parent: ttk.Frame) -> None:
        filt = ttk.Frame(parent); filt.pack(fill="x", pady=6, padx=8)
        ttk.Label(filt, text="Search:").pack(side="left")
        self.search_var = tk.StringVar(); ttk.Entry(filt, textvariable=self.search_var, width=40).pack(side="left", padx=6)
        ttk.Label(filt, text="Type:").pack(side="left", padx=(12, 4))
        self.type_var = tk.StringVar(value="All")
        ttk.Combobox(filt, textvariable=self.type_var, values=["All", "Weapon", "Equipment", "Equipment Alt", "Special"], width=18, state="readonly").pack(side="left")
        ttk.Button(filt, text="Filter", command=self.apply_filter).pack(side="left", padx=6)
        ttk.Button(filt, text="Export Decoded → YAML", command=self.export_decoded_yaml).pack(side="left", padx=12)

        cols = ("path", "type", "code", "serial")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings")
        for c, txt, w in [("path", "Path", 520), ("type", "Type", 140), ("code", "Code", 80), ("serial", "Serial", 540)]:
            self.tree.heading(c, text=txt)
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(expand=True, fill="both", padx=8, pady=(0, 8))
        self.tree.bind("<Double-1>", self.open_inspector)
        self.tree.bind("<Button-3>", self._on_tree_right_click)  # Add right click handler

        # Context menu for Serial column
        self.serial_menu = tk.Menu(self.tree, tearoff=0)
        self.serial_menu.add_command(label="Copy Serial", command=self._copy_serial_to_clipboard)

    def _on_tree_right_click(self, event):
        # Identify which row and column was clicked
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        col = self.tree.identify_column(event.x)
        if col != "#4":  # "#4" is the serial column (1-based index)
            return
        rowid = self.tree.identify_row(event.y)
        if not rowid:
            return

        self.tree.selection_set(rowid)
        self._serial_rowid = rowid  # Store for menu callback
        self.serial_menu.tk_popup(event.x_root, event.y_root)

    def _copy_serial_to_clipboard(self):
        rowid = getattr(self, "_serial_rowid", None)
        if not rowid:
            return
        values = self.tree.item(rowid, "values")
        if len(values) < 4:
            return
        serial = values[3]
        self.root.clipboard_clear()
        self.root.clipboard_append(serial)
        self.root.update()  # Keeps clipboard contents after app closes
        mb.showinfo("Copied", "Serial copied to clipboard.")

    # ... (rest of your class unchanged) ...
