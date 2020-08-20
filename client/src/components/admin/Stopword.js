import React, { useState, useEffect } from "react";
import "./Stopword.scss";
import "../Common.scss";
import axios from "axios";
import config from "../../settings/config.json";

// Table
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import TablePagination from "@material-ui/core/TablePagination";

const Stopword = () => {
  const [stopwords, setStopwords] = useState([]);

  const columns = [
    {
      id: "word",
      label: "불용어",
      align: "center",
    },
  ];

  const useStyles = makeStyles({
    root: {
      width: "100%",
      height: "100%",
      alignSelf: "center",
    },
    container: {
      minHeight: "90%",
      maxHeight: "90%",
      width: "100%",
    },
    pagination: {
      maxHeight: "10%",
      width: "100%",
    },
  });

  const classes = useStyles();

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  // Load wordcloud when this page is rendered.
  useEffect(() => {
    console.log("Stopword rendered!");
    axios
      .get("http://" + config.host + ":" + config.port + "/stopword")
      .then((response) => {
        let stopwords = response.data["results"];
        console.log(stopwords);

        let stopwords_formatted = stopwords.map((stopword, index) => ({
          id: index,
          word: stopword,
        }));
        setStopwords(stopwords_formatted);
      })
      .catch((response) => {
        console.log(response);
      });
  }, []);

  return (
    <div className="Container">
      <div className="StopwordContainer">
        <div className="ContainerHeader">
          <div className="ContainerTitle">Stopword</div>
          <div className="SizedBox"></div>
        </div>
        <div className="ContainerContent">
          <Paper className={classes.root}>
            <TableContainer className={classes.container}>
              <Table stickyHeader aria-label="sticky table">
                <TableHead>
                  <TableRow>
                    {columns.map((column) => (
                      <TableCell key={column.id} align={column.align} style={{ minWidth: column.minWidth }}>
                        {column.label}
                      </TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {stopwords.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((stopword) => {
                    return (
                      <TableRow hover role="checkbox" tabIndex={-1} key={stopword.id}>
                        <TableCell>{stopword.word}</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              className={classes.pagination}
              rowsPerPageOptions={[5, 10]}
              component="div"
              count={stopwords.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onChangePage={handleChangePage}
              onChangeRowsPerPage={handleChangeRowsPerPage}
            />
          </Paper>
        </div>
      </div>
    </div>
  );
};

export default Stopword;
