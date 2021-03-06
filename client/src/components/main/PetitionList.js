import React, { useState, useEffect, useContext } from "react";
import "./PetitionList.scss";
import axios from "axios";
import config from "../../settings/config.json";
import KeywordContext from "../../context/Keyword.context";

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

const PetitionList = () => {
  // Define state of wordcloud data
  const [petitions, setPetitions] = useState([]);
  const [isSelectWord, setIsSelectWord] = useState(false);
  const { word } = useContext(KeywordContext);

  const columns = [
    {
      id: "title",
      label: "제목",
      align: "left",
      minWidth: 250,
    },
    {
      id: "url",
      label: "URL",
      align: "left",
      minWidth: 50,
    },
  ];

  const useStyles = makeStyles({
    root: {
      width: "100%",
      height: "100%",
      alignSelf: "center",
    },
    container: {
      minHeight: "80%",
      maxHeight: "80%",
      width: "100%",
    },
    pagination: {
      maxHeight: "20%",
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
    if (word !== "DefaultWord") {
      axios
        .get("http://" + config.host + ":" + config.port + "/petition?keyword=" + word + "&interval=30")
        .then((response) => {
          let petitions = response.data["results"];
          let petitions_formatted = petitions.map((petition) => ({
            title: petition["title"],
            url: petition["url"],
          }));
          console.log(petitions_formatted);

          setPetitions(petitions_formatted);
          setIsSelectWord(true);
        })
        .catch((response) => {
          console.log(response);
        });
    }
  }, [word]);

  return (
    <div className="wrap">
      {isSelectWord ? (
        <div className="wrap-petitionlist">
          <div className="petitionlist-header">
            <div className="header-title">'{word}' 단어가 포함된 청원 목록 (최근 30일)</div>
          </div>
          <div className="petitionlist-content">
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
                    {petitions.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((petition) => {
                      return (
                        <TableRow hover role="checkbox" tabIndex={-1} key={petition.title}>
                          <TableCell>{petition.title}</TableCell>
                          <TableCell>
                            <a href={petition.url} target="_blank" rel="noopener noreferrer">
                              {petition.url}
                            </a>
                          </TableCell>
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
                count={petitions.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onChangePage={handleChangePage}
                onChangeRowsPerPage={handleChangeRowsPerPage}
              />
            </Paper>
          </div>
        </div>
      ) : (
        "위쪽의 워드클라우드에서 단어를 선택해주세요"
      )}
    </div>
  );
};

export default PetitionList;
